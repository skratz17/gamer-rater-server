"""Games ViewSet and Serializer"""
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from raterapp.models import Game, Category, Designer, GameCategory, GameImage

class Games(ViewSet):
    """Games ViewSet"""

    def create(self, request):
        """POST new game"""
        # TODO: implement more validation!
        game = Game()

        try:
            category = Category.objects.get(pk=request.data['categoryId'])
        except Category.DoesNotExist:
            return Response(
                {'message': '`categoryId` provided does not match an existing Category.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            designer = Designer.objects.get(pk=request.data['designerId'])
        except Designer.DoesNotExist:
            return Response(
                {'message': '`designerId` provided does not match an existing Designer.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        game.title = request.data['title']
        game.description = request.data['description']
        game.year = request.data['year']
        game.num_players = request.data['numPlayers']
        game.estimated_duration = request.data['estimatedDuration']
        game.age_recommendation = request.data['ageRecommendation']
        game.designer = designer

        game.save()

        game_category = GameCategory()
        game_category.game = game
        game_category.category = category

        game_category.save()

        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """GET game by id"""
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        game.categories = GameCategory.objects.filter(game=game)
        game.images = GameImage.objects.filter(game=game)

        serialized_game = GameSerializer(game, context={'request': request})
        return Response(serialized_game.data)

    def list(self, request):
        """GET all games"""
        # TODO: implement searching/filtering by query string param here
        games = Game.objects.all()

        search_term = self.request.query_params.get('q', None)
        if search_term is not None:
            games = games.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(designer__name__icontains=search_term)
            )

        # Map query string parameter orderby values to property to actually
        # order by in query
        orderable_fields_dict = {
            "year": "year",
            "duration": "estimated_duration",
            "designer": "designer__name"
        }

        order_by = self.request.query_params.get('orderby', None)
        if order_by is not None and order_by in orderable_fields_dict:
            games = games.order_by(orderable_fields_dict[order_by])

        serializer = MinimalGameSerializer(games, many=True, context={'request': request})
        return Response(serializer.data)

class MinimalGameSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for only game name, id, and url"""

    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(
            view_name="game",
            lookup_field="id"
        )
        fields = ('id', 'url', 'title', 'average_rating')

class DesignerSerializer(serializers.ModelSerializer):
    """JSON serializer for designer"""

    class Meta:
        model = Designer
        fields = ('id', 'name')

class GameCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for game_category objects"""
    class Meta:
        model = GameCategory
        fields = ('id', 'category')
        depth = 1

class GameImageSerializer(serializers.ModelSerializer):
    """JSON serializer for game_image objects"""
    class Meta:
        model = GameImage
        fields = ('id', 'image')

class GameSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for full game object"""
    designer = DesignerSerializer(many=False)
    categories = GameCategorySerializer(many=True)
    images = GameImageSerializer(many=True)

    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(
            view_name='game',
            lookup_field='id'
        )

        fields = (
            'id', 'url', 'title', 'description', 'year', 'num_players', 'images',
            'estimated_duration', 'age_recommendation', 'designer', 'categories', 'average_rating'
        )

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
        categories = []

        for category_id in request.data['categories']:
            try:
                category = Category.objects.get(pk=category_id)
                categories.append(category)

            except Category.DoesNotExist:
                return Response(
                    {'message': 'A categoryId in `categories` provided does not match an existing Category.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            designer = Designer.objects.get(pk=request.data['designerId'])
        except Designer.DoesNotExist:
            return Response(
                {'message': '`designerId` provided does not match an existing Designer.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        game = Game()

        game.title = request.data['title']
        game.description = request.data['description']
        game.year = request.data['year']
        game.num_players = request.data['numPlayers']
        game.estimated_duration = request.data['estimatedDuration']
        game.age_recommendation = request.data['ageRecommendation']
        game.designer = designer

        game.save()

        for category in categories:
            game_category = GameCategory(game=game, category=category)
            game_category.save()

        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        categories = []

        for category_id in request.data['categories']:
            try:
                category = Category.objects.get(pk=category_id)
                categories.append(category)

            except Category.DoesNotExist:
                return Response(
                    {'message': 'A category id in `categories` provided does not match an existing Category.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            designer = Designer.objects.get(pk=request.data['designerId'])
        except Designer.DoesNotExist:
            return Response(
                {'message': '`designerId` provided does not match an existing Designer.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response(
                {'message': 'The game attempting to be accessed does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )

        game.title = request.data['title']
        game.description = request.data['description']
        game.year = request.data['year']
        game.num_players = request.data['numPlayers']
        game.estimated_duration = request.data['estimatedDuration']
        game.age_recommendation = request.data['ageRecommendation']
        game.designer = designer

        game.save()

        current_game_categories = GameCategory.objects.filter(game=game)

        # Delete GameCategories that no longer apply to this game
        current_game_categories.filter(~Q(category__in=categories)).delete()

        # Save new GameCategories for this game
        for category in categories:
            try:
                current_game_categories.get(category=category)

            except GameCategory.DoesNotExist:
                game_category = GameCategory(game=game, category=category)
                game_category.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

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
            order_field = orderable_fields_dict[order_by]

            direction = self.request.query_params.get('direction', 'asc')
            if direction == 'desc':
                order_field = '-' + order_field

            games = games.order_by(order_field)

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

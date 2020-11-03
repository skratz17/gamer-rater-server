"""Games ViewSet and Serializer"""
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from raterapp.models import Game, Category, Designer, GameCategory

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
                status=HTTP_400_BAD_REQUEST
            )

        try:
            designer = Designer.objects.get(pk=request.data['designerId'])
        except Designer.DoesNotExist:
            return Response(
                {'message': '`designerId` provided does not match an existing Designer.'},
                status=HTTP_400_BAD_REQUEST
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

        return Response(status=HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """GET game by id"""
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        game_categories = GameCategory.objects.filter(game=game)

        serialized_game = GameSerializer(game, context={'request': request})
        serialized_categories = GameCategorySerializer(
            game_categories, many=True, context={'request': request}
        )

        response = {
            **serialized_game.data,
            'categories': serialized_categories.data
        }

        return Response(response)

    def list(self, request):
        """GET all games"""
        # TODO: implement searching/filtering by query string param here
        games = Game.objects.all()

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
        fields = ('id', 'url', 'title')

class DesignerSerializer(serializers.ModelSerializer):
    """JSON serializer for designer"""

    class Meta:
        model = Designer
        fields = ('id', 'name')

class GameSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for full game object"""
    designer = DesignerSerializer(many=False)

    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(
            view_name='game',
            lookup_field='id'
        )

        fields = ('id', 'url', 'title', 'description', 'year', 'num_players', 'estimated_duration', 'age_recommendation', 'designer')

class GameCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for game_category objects"""
    class Meta:
        model = GameCategory
        fields = ('id', 'category')
        depth = 1
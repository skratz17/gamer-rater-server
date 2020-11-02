"""Games ViewSet and Serializer"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from raterapp.models import Game

class Games(ViewSet):
    """Games ViewSet"""

    def retrieve(self, request, pk=None):
        """GET game by id"""
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """GET all games"""
        # TODO: implement searching/filtering by query string param here
        games = Game.objects.all()

        serializer = GameSerializer(games, many=True, context={'request': request})
        return Response(serializer.data)

class GameSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for games"""

    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(
            view_name='game',
            lookup_field='id'
        )

        # TODO: add designer field once serializer implemented for designer
        fields = ('id', 'url', 'title', 'description', 'year', 'num_players', 'estimated_duration', 'age_recommendation')

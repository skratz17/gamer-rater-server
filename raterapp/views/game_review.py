"""Game Review ViewSet and Serializers"""
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from raterapp.models import GameReview, Game, Player

class GameReviews(ViewSet):
    """ViewSet class for GameReviews"""

    def list(self, request):
        reviews = GameReview.objects.all()

        game_id = self.request.query_params.get('gameId', None)
        if game_id is not None:
            reviews = reviews.filter(game__id=game_id)

        serialization = GameReviewSerializer(reviews, many=True)

        return Response(serialization.data, status=status.HTTP_200_OK)

class GameReviewUserSerializer(serializers.ModelSerializer):
    """JSON serializer for user nested in a review (via player)"""
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')

class GameReviewGameSerializer(serializers.ModelSerializer):
    """JSON serializer for game nested in a review"""
    class Meta:
        model = Game
        fields = ('id', 'title', 'year')

class GameReviewPlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for player nested in a review"""
    user = GameReviewUserSerializer(many=False)

    class Meta:
        model = Player
        fields = ('user', )

class GameReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for review"""
    game = GameReviewGameSerializer(many=False)
    player = GameReviewPlayerSerializer(many=False)

    class Meta:
        model = GameReview
        fields = ('rating', 'review', 'timestamp', 'game', 'player')

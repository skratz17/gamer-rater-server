"""Game Review ViewSet and Serializers"""
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from raterapp.models import GameReview, Game, Player

class GameReviews(ViewSet):
    """ViewSet class for GameReviews"""

    def list(self, request):
        """GET all reviews (optionally filter by gameId query string param)"""
        reviews = GameReview.objects.all()

        game_id = self.request.query_params.get('gameId', None)
        if game_id is not None:
            reviews = reviews.filter(game__id=game_id)

        serialization = GameReviewSerializer(reviews, many=True)

        return Response(serialization.data, status=status.HTTP_200_OK)

    def create(self, request):
        """POST a new review"""

        # TODO: more validation!!
        player = Player.objects.get(user=request.auth.user)

        try:
            game = Game.objects.get(pk=request.data["gameId"])
        except Game.DoesNotExist:
            return Response(
                {'message': 'There is no game with the supplied gameId.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        review = GameReview()
        review.player = player
        review.game = game
        review.rating = request.data["rating"]
        review.review = request.data["review"]
        review.timestamp = request.data["timestamp"]

        review.save()

        return Response({}, status=status.HTTP_201_CREATED)

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
        fields = ('id', 'user', )

class GameReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for review"""
    game = GameReviewGameSerializer(many=False)
    player = GameReviewPlayerSerializer(many=False)

    class Meta:
        model = GameReview
        fields = ('id', 'rating', 'review', 'timestamp', 'game', 'player')

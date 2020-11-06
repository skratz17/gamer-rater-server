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

        # Verify that all required keys are present in POST body
        missing_keys = self._get_missing_keys(request.data)
        if len(missing_keys) > 0:
            return Response(
                {'message':
                    f'Request body is missing the following required properties: {", ".join(missing_keys)}'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

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

    def _get_missing_keys(self, data):
        """Given the request.data for a POST/PUT request, return a list containing the
        string values of all required keys that were not found in the request body"""
        REQUIRED_KEYS = [ 'rating', 'review', 'timestamp', 'gameId' ]

        return [ key for key in REQUIRED_KEYS if not key in data ]

class GameReviewGameSerializer(serializers.ModelSerializer):
    """JSON serializer for game nested in a review"""
    class Meta:
        model = Game
        fields = ('id', 'title', 'year')

class GameReviewPlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for player nested in a review"""
    class Meta:
        model = Player
        fields = ('id', 'full_name')

class GameReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for review"""
    game = GameReviewGameSerializer(many=False)
    player = GameReviewPlayerSerializer(many=False)

    class Meta:
        model = GameReview
        fields = ('id', 'rating', 'review', 'timestamp', 'game', 'player')

"""Game Image ViewSet and Serializer"""
from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
import uuid
import base64
from raterapp.models import GameImage, Game, Player

class GameImages(ViewSet):
    """Game Images ViewSet"""

    def create(self, request):
        """POST a new image"""
        # Validate that all required keys are present in request body
        missing_keys = self._get_missing_keys()
        if len(missing_keys) > 0:
            return Response(
                {'message':
                    f'Request body is missing the following required properties: {", ".join(missing_keys)}'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            game = Game.objects.get(pk=request.data["gameId"])
        except Game.DoesNotExist:
            return Response(
                {'message': 'There is no game with the supplied gameId.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        player = Player.objects.get(user=request.auth.user)

        image = GameImage()

        image.game = game
        image.player = player

        try:
            fmt, imgstr = request.data["image"].split(';base64,')
        except ValueError:
            return Response(
                {'message': 'The image value must be in valid base64 format, please try again.'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        ext = fmt.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["gameId"]}-{uuid.uuid4()}.{ext}')

        image.image = data
        image.save()

        return Response({}, status=status.HTTP_201_CREATED)

    def _get_missing_keys(self):
        """Given the request.data for a POST/PUT request, return a list containing the
        string values of all required keys that were not found in the request body"""
        REQUIRED_KEYS = [ 'gameId', 'image' ]

        return [ key for key in REQUIRED_KEYS if not key in self.request.data ]

class GameImageSerializer(serializers.ModelSerializer):
    """JSON serializer for GameImage"""
    class Meta:
        model = GameImage
        fields = ('id', 'image')

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
        image = GameImage()

        try:
            game = Game.objects.get(pk=request.data["gameId"])
        except Game.DoesNotExist:
            return Response(
                {'message': 'There is no game with the supplied gameId.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        player = Player.objects.get(user=request.auth.user)

        image.game = game
        image.player = player

        fmt, imgstr = request.data["image"].split(';base64,')
        ext = fmt.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["gameId"]}-{uuid.uuid4()}.{ext}')

        image.image = data
        image.save()

        return Response({}, status=status.HTTP_201_CREATED)

class GameImageSerializer(serializers.ModelSerializer):
    """JSON serializer for GameImage"""
    class Meta:
        model = GameImage
        fields = ('id', 'image')

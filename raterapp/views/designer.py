"""Designer ViewSet and Serializers"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterapp.models import Designer

class Designers(ViewSet):
    """Designer ViewSet"""

    def list(self, request):
        designers = Designer.objects.all()
        serialization = DesignerSerializer(designers, many=True)
        return Response(serialization.data)

class DesignerSerializer(serializers.ModelSerializer):
    """JSON serializer for designer"""

    class Meta:
        model = Designer
        fields = ('id', 'name')

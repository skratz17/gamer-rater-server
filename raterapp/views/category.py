"""Category ViewSet and Serializers"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from raterapp.models import Category

class Categories(ViewSet):
    """Category Viewset"""
    def retrieve(self, request, pk=None):
        """GET single category by id"""
        try:
            category = Category.objects.get(pk=pk)

        except Category.DoesNotExist:
            return Response(
                { 'message': 'There is no category with the specified ID.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        serialization = CategorySerializer(category)
        return Response(serialization.data)

    def list(self, request):
        """GET all categories"""
        categories = Category.objects.all()
        serialization = CategorySerializer(categories, many=True)
        return Response(serialization.data)

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for category"""

    class Meta:
        model = Category
        fields = ('id', 'name')
        
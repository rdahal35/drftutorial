from .models import Product, Review
from rest_framework import serializers


class ReviewSerializers(serializers.ModelSerializer):
    created_by= serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model= Review
        fields= ('id', 'title', 'review', 'rating','created_by')




class ProductSerializers(serializers.ModelSerializer):

    reviews =ReviewSerializers(many=True, read_only=True)

    class Meta:
        model= Product
        fields= ('id', 'name', 'description', 'price', 'reviews')


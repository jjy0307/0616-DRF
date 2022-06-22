from rest_framework import serializers
from .models import Product as ProductModel


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['author', 'title', 'discription', 'view_start_date', 'view_end_date']

from functools import partial
from django.shortcuts import render
from django.utils import timezone
from product.serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from product.models import Product as ProductModel
from django.db.models.query_utils import Q


# Create your views here.

class ProductView(APIView):
    def post(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({"error": "로그인 후 이용해주세요"}, status=status.HTTP_400_BAD_REQUEST)
        print(request.data)
        # request.data['author'] = user.id
        # print(request.data)
        product_serializer = ProductSerializer(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=200)

        return Response(product_serializer.errors, status=400)

    def put(self, request, obj_id):
        product = ProductModel.objects.get(id=obj_id)
        product_serializer = ProductSerializer(product, data=request.data, partial=True)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=200)

        return Response(product_serializer.errors, status=400)


class TimeValidOrUserValidProduct(APIView):
    def get(self, request):
        user = request.user
        today = timezone.now()
        products = ProductModel.objects.filter(
            Q(view_start_date__lte=today, view_end_date__gte=today) | Q(author=user)
        )
        filter_serializer = ProductSerializer(products, many=True).data

        return Response(filter_serializer, status=200)
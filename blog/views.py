from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from drf2.permissions import RegistedMoreThanAThreeDayUser as R
from drf2.permissions import IsAdminOrIsAuthenticatedReadOnly as I
from blog.models import Article as ArticleModel
from user.serializers import ArticleSerializer
from rest_framework import status


# Create your views here.
class MakeArticle(APIView):
    # permission_classes = [I]
    def get(self, request):
        filter_sort_article = ArticleModel.objects.filter(view_start_day__gt='2022-06-12',
                                                          view_start_day__lte='2022-06-20').order_by('upload_date')

        return Response({'message': 'article is filtered and sorted'})

    def post(self, request):
        user = request.user
        request.data['author'] = user.id
        article_serializer = ArticleSerializer(data=request.data)
        if article_serializer.is_valid():  # True or False
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)

        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from unicodedata import category
from rest_framework import serializers
from .models import CustomUser as CustomUserModel
from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel
from blog.models import Category as CategoryModel


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['article', 'contents']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['name', 'discription']


class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    # default create는 모든 외래키에 대해시 성립을 하지 않으므로 custom create를 만들어야한다.
    comments = CommentSerializer(many=True, source='commnent_set', read_only=True)

    def get_category(self, obj):
        return [category.name for category in obj.category.all()]

    class Meta:
        model = ArticleModel
        fields = ['name', 'content', 'category', 'comments', 'author']


class CustomUserSerializer(serializers.ModelSerializer):
    article_set = ArticleSerializer(many=True, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUserModel
        fields = ['username', 'join_date', 'article_set', 'comment_set']

        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
            'password': {'write_only': True},  # default : False
            'email': {
                # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
                'error_messages': {
                    # required : 값이 입력되지 않았을 때 보여지는 메세지
                    'required': '이메일을 입력해주세요.',
                    # invalid : 값의 포맷이 맞지 않을 때 보여지는 메세지
                    'invalid': '알맞은 형식의 이메일을 입력해주세요.'
                },
                # required : validator에서 해당 값의 필요 여부를 판단한다.
                'required': False  # default : True
            },
        }
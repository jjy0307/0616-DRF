from django.contrib import admin
from blog.models import Category
from .models import Article
from .models import Comment

# Register your models here.
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)
from distutils.command.upload import upload
from django.db import models
from user.models import CustomUser


# Create your models here.
class Product(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to=None, height_field=None, width_field=None, null=True)
    discription = models.TextField(max_length=500)
    add_date = models.DateField(auto_now_add=True)
    view_start_date = models.DateField(null=True)
    view_end_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.author} / {self.title}'
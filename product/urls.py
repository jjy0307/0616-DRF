from django.urls import path
from product import views

urlpatterns = [
    path('', views.ProductView.as_view()),
    path('filter/', views.TimeValidOrUserValidProduct.as_view()),
    path('<obj_id>/', views.ProductView.as_view()),
]
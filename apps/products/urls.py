from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('category', views.CategoryList.as_view(), name='category_all'),
]
from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('category/', views.CategoryFilteredListCreateAPI.as_view(), name='category_list_all_create'),
    path('category/<pk>/', views.CategoryReadDeleteUpdateAPI.as_view(), name='category_read_dlt_update'),
    path('product/', views.ProductFilteredListCreateAPI.as_view(), name='product_list_all_create'),
    path('product/<pk>/', views.ProductReadDeleteUpdateAPI.as_view(), name='product_read_dlt_update'),
]
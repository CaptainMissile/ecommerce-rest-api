
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend

from config.paginations import PagePagination
from apps.products.models import Category, ProductInventory
from apps.products.serializers import (CategorySerializer,
                                      ProductInventorySerializer)


class CategoryFilteredListCreateAPI(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'slug']
    

class CategoryReadDeleteUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

class ProductFilteredListCreateAPI(generics.ListCreateAPIView):
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer
    pagination_class = PagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id' , 'store', 'price', 'is_active','created_at',
                        'updated_at']


class ProductReadDeleteUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer
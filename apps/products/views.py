from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend


from config.paginations import PagePagination
from apps.products.models import Category, ProductInventory
from apps.products.permissions import (ReadOrIsSeller, ReadOrIsAdmin,
                                        IsAllowedToChangeInventory)
from apps.products import serializers


class CategoryFilteredListCreateAPI(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    pagination_class = PagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'slug']


class CategoryReadDeleteUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ReadOrIsAdmin]
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    

class ProductFilteredListCreateAPI(generics.ListCreateAPIView):
    permission_classes = [ReadOrIsSeller]
    serializer_class = serializers.ProductInventorySerializer
    pagination_class = PagePagination
    

    def get_queryset(self):
        filter_params = self._get_filter_params(self.request.query_params)

        return ProductInventory.objects.filter(**filter_params).order_by('-created_at')
    

    def _get_filter_params(self, query_params):
        filterset_fields = ['id' , 'store', 'category', 'price', 'is_active',
                            'created_at', 'updated_at']

        params_dict = dict()

        for param in query_params:
            if param in filterset_fields:
                if param == 'id' or param == 'units_sold' or param == 'units': 
                    params_dict[param] = int(query_params[param])
                elif param == 'price':
                    params_dict['price'] = float(query_params[param])
                elif param == 'store':
                    params_dict['store__id'] = int(query_params[param])
                elif param == 'category':
                    params_dict['category__name'] = query_params[param]
                elif param == 'is_active':
                    params_dict[param] = True if query_params[param].lower() == 'true' else False
        

        return params_dict


class ProductReadDeleteUpdateAPI(views.APIView):
    permission_classes = [IsAllowedToChangeInventory]

    def get(self, request, id):
        product = ProductInventory.objects.get(id = id)
        self.check_object_permissions(request, product) 
        serializer = serializers.ProductInventorySerializer(product)
        return Response(serializer.data,
                        status = status.HTTP_200_OK)

    def delete(self, request, id):
        product = ProductInventory.objects.get(id = id)
        self.check_object_permissions(request, product)
        product.delete() 

        return Response({'msg' : 'Successfully Deleted!'},
                        status = status.HTTP_200_OK)


    def patch(self, request, id):
        product = ProductInventory.objects.get(id = id)
        self.check_object_permissions(request, product)
        serializer = serializers.ProductInventorySerializer(instance = product,
                                                data = request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status = status.HTTP_200_OK)

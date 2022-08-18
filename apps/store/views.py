from django.conf import settings

from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.views import APIView, Response
from rest_framework.generics import ListAPIView
from rest_framework import status

from config.paginations import PagePagination
from apps.store.permissions import IsSeller, IsAuthenticatedStoreOwner
from apps.store.serializers import StoreSerializer, StoreUpdateSerializer
from apps.store.models import Store
# Create your views here.

# CREATE STORE
# UPDATE STORE INFO
# DELETE STORE
# READ SINGLE STORE INFO
# READ ALL THE STORE INFO
# STORE INFO FILTERED BY OWNER OR PRODUCT OR CATEGORY OR STORE NAME

class StoreCreateAPI(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request):
        store_data = request.data
        store_data['owner'] = request.user.id

        serializer = StoreSerializer(data = store_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({'msg': 'Successfully Store Created'},
                            status= status.HTTP_201_CREATED)

        return Response({'error': 'Something Went wrong.Try again'})


class StoreUpdateAPI(APIView):
    permission_classes = [IsAuthenticated, IsAuthenticatedStoreOwner]

    def put(self, request, store_id, format=None):
        try:
            store_instance = Store.objects.get(id = store_id)
        except:
            return Response({'error':'Store does not exist'}, status = status.HTTP_400_BAD_REQUEST)

        self.check_object_permissions(request, store_instance) 

        serializer = StoreUpdateSerializer(
                            instance= store_instance,
                            data = request.data,
                            partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Store Info Updated'}, status = status.HTTP_200_OK)
    
        return Response({'error':'You are not authorized to make this change'}, status = status.HTTP_400_BAD_REQUEST)



class StoreDeleteAPI(APIView):
    permission_classes = [IsAuthenticated, IsAuthenticatedStoreOwner]

    def delete(self, request, store_id, format=None):
        try:
            store_instance = Store.objects.get(id = store_id)
        except:
            return Response({'error':'Store does not exist'}, status = status.HTTP_400_BAD_REQUEST)
        
        self.check_object_permissions(request, store_instance)

        store_instance.delete()
        return Response({'msg': 'Store Deleted'}, status = status.HTTP_200_OK)


        
class StoreSingleAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, store_id):
        try:
            store_instance = Store.objects.get(id = store_id)
        except:
            return Response({'error':'Store does not exist'}, status = status.HTTP_400_BAD_REQUEST)

        serializer = StoreSerializer(store_instance)
        return Response(serializer.data, status= status.HTTP_200_OK)


class StoreListAPI(ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PagePagination



class StoreFilteredListAPI(APIView):
    '''FILTER WITH
            1. OWNER
            2. NAME
    '''
    def get(request):
        pass
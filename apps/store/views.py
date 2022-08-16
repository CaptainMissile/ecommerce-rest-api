from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from rest_framework import status

from apps.store.permissions import IsSeller
from apps.store.serializers import StoreSerializer
# Create your views here.

# CREATE STORE
# UPDATE STORE INFO
# DELETE STORE
# READ SINGLE STORE INFO
# READ ALL THE STORE INFO
# STORE INFO FILTERED BY OWNER OR PRODUCT OR CATEGORY OR STORE NAME

class StoreCreateAPI(views.APIView):
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


class StoreUpdateAPI(views.APIView):
    def post(request):
        pass

class StoreDeleteAPI(views.APIView):
    def post(request):
        pass

class StoreListAPI(views.APIView):
    def get(request):
        pass

class StoreSingleAPI(views.APIView):
    def get(request):
        pass

class StoreFilteredListAPI(views.APIView):
    def get(request):
        pass
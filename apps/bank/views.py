from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.views import APIView, Response
from rest_framework import status

from apps.store.permissions import IsSeller, IsAuthenticatedStoreOwner
from apps.bank.serializers import (BankAccountSerializer, TransactionSerializer,
                                    BankAccountUpdateSerializer)

from apps.bank.models import BankOption, BankAccount, Transaction
from apps.store.models import Store
from apps.accounts.models import Profile
# Create your views here.

class BankAccountCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        acc_obj = BankOption.objects.get(key= 'account_no')
        acc_no = acc_obj.value + 1
        acc_obj.value = acc_no
        acc_obj.save()

        bank_account_data = request.data
        bank_account_data['account_no'] = acc_no

        serializer = BankAccountSerializer(data = bank_account_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            msg = "Bank Account Created"
            try:
                profile = Profile.objects.get(user = request.user.id)
                profile.bank_account = acc_no
                profile.save()

                msg += " And Your Profile Updated!"
            except:
                msg += " And No Profile Updated!"
            
            return Response({'msg': msg}, status= status.HTTP_201_CREATED)

        return Response({'error': 'Something Went wrong.Try again'})


class BankAccountUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, account_no, format=None):
        try:
            account_instance = BankAccount.objects.get(id = account_no)
        except:
            return Response({'error':'Bank Account does not exist'}, status = status.HTTP_400_BAD_REQUEST)

        self.check_object_permissions(request, account_instance) 

        serializer = BankAccountUpdateSerializer(
                            instance= account_instance,
                            data = request.data,
                            partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Bank Account Info Updated'}, status = status.HTTP_200_OK)
    
        return Response({'error':'You are not authorized to make this change'}, status = status.HTTP_400_BAD_REQUEST)



# class StoreDeleteAPI(views.APIView):
#     permission_classes = [IsAuthenticated, IsAuthenticatedStoreOwner]

#     def delete(self, request, store_id, format=None):
#         try:
#             store_instance = Store.objects.get(id = store_id)
#         except:
#             return Response({'error':'Store does not exist'}, status = status.HTTP_400_BAD_REQUEST)
        
#         self.check_object_permissions(request, store_instance)

#         store_instance.delete()
#         return Response({'msg': 'Store Deleted'}, status = status.HTTP_200_OK)


        
# class StoreSingleAPI(views.APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request, store_id):
#         try:
#             store_instance = Store.objects.get(id = store_id)
#         except:
#             return Response({'error':'Store does not exist'}, status = status.HTTP_400_BAD_REQUEST)

#         serializer = StoreSerializer(store_instance)
#         return Response(serializer.data, status= status.HTTP_200_OK)


# class StoreListAPI(views.APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request):
#         store_instances = Store.objects.all()
#         serializer = StoreSerializer(store_instances, many=True)
#         return Response(serializer.data, status= status.HTTP_200_OK)


# class StoreFilteredListAPI(views.APIView):
#     '''FILTER WITH
#             1. OWNER
#             2. NAME
#     '''
#     def get(request):
#         pass
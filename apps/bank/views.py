from ast import Raise
from logging import raiseExceptions
from typing import List
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.views import APIView, Response
from rest_framework.generics import ListAPIView
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from config.paginations import PagePagination
from apps.bank.permissions import (IsBankAccountOwnerOrManager,
                            IsBankManager)
from apps.bank.serializers import (BankAccountSerializer,
                                   BankAccountUpdateSerializer,
                                   AddMoneyRequestSerializer,
                                   SendMoneyRequestSerializer,
                                   TransactionSerializer)

from apps.bank.models import BankOption, BankAccount, Transaction
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
    permission_classes = [IsAuthenticated, IsBankAccountOwnerOrManager]

    def put(self, request, account_no, format=None):
        try:
            account_instance = BankAccount.objects.get(account_no = account_no)
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




class BankAccountDeleteAPI(APIView):
    permission_classes = [IsAuthenticated, IsBankAccountOwnerOrManager]

    def delete(self, request, account_no, format=None):
        try:
            acc_instance = BankAccount.objects.get(account_no = account_no)

            profile = Profile.objects.get(user__id = request.user.id) 
            profile.bank_account = None
            profile.save()
        except:
            return Response({'error':'Bank Account does not exist'}, status = status.HTTP_400_BAD_REQUEST)
        
        self.check_object_permissions(request, acc_instance)
        acc_instance.delete()

        return Response({'msg': 'Bank Account Deleted'}, status = status.HTTP_200_OK)


        
class BankAccountSingleAPI(APIView):
    permission_classes = [IsAuthenticated, IsBankAccountOwnerOrManager]

    def get(self, request, account_no):
        try:
            acc_instance = BankAccount.objects.get(id = account_no)
        except:
            return Response({'error':'Bank Account does not exist'}, status = status.HTTP_400_BAD_REQUEST)

        serializer = BankAccountSerializer(acc_instance)
        return Response(serializer.data, status= status.HTTP_200_OK)


class BankAccountListAPI(ListAPIView):
    permission_classes = [IsAuthenticated,IsBankManager]
    serializer_class = BankAccountSerializer
    pagination_class = PagePagination


class AddMoneyToAccountRequestAPI(APIView):
    def post(self, request):
        serializer = AddMoneyRequestSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Money Added Request Sent Successfully.'},
                            status = status.HTTP_200_OK)
        
        return Response({"error" : "Money Add Request Can't be sent!"})


class SendMoneyToAccountRequestAPI(APIView):
    def post(self, request):
        serializer = SendMoneyRequestSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Send Money Request Sent Successfully.'},
                            status = status.HTTP_200_OK)
        
        return Response({"error" : "Money Add Request Can't be sent!"})


class TransactionSingleAPI(APIView):
    def get(self,request, transaction_id):
        try:
            transaction = Transaction.objects.get(id = transaction_id)
            serialiazer = TransactionSerializer(transaction)
            return Response(serialiazer.data, status.HTTP_200_OK)
        except:
            return Response({'error': 'Somethimg went wrog!'},
                            status = status.HTTP_400_BAD_REQUEST)




class TransactionListAPI(ListAPIView):
        permission_classes = [IsAuthenticated,IsBankManager]
        queryset = Transaction.objects.all()
        serializer_class = TransactionSerializer
        pagination_class = PagePagination


class TransactionFilterAPI(ListAPIView):
    permission_classes = [IsAuthenticated,IsBankManager]
    queryset = Transaction.objects.all().order_by('-created_at')
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'account_from', 'account_to','status', 'type',
                        'created_at', 'is_approved', 'approved_by']


class ApproveCashInRequestAPI(APIView):
    permission_classes = [IsAuthenticated, IsBankManager]

    def get(self, request, transaction_id):
        transaction = Transaction.objects.get(id = transaction_id)

        try:
            if transaction.type == 'I' and transaction.is_approved == False:
                account_to = BankAccount.objects.get(account_no = transaction.account_to.account_no)
                cur_balance =  account_to.balance + transaction.amount
                account_to.balance = cur_balance
                transaction.is_approved = True
                transaction.approved_by = request.user
                transaction.status = 'A'

                transaction.save()
                account_to.save()
            else:
                return Response({'error' : 'Sorry Something Went Wrong!'},
                            status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error' : 'Sorry Something Went Wrong!'},
                            status = status.HTTP_400_BAD_REQUEST)

        
        return Response({'msg': 'Your Cash In Request Successfully Approved'},
                        status = status.HTTP_200_OK)



class ApproveSendMoneyRequestAPI(APIView):
    def get(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id = transaction_id)
            
            if transaction.type == 'S' and transaction.is_approved == False:
                account_from = BankAccount.objects.get(account_no = transaction.account_from.account_no)
                account_to = BankAccount.objects.get(account_no = transaction.account_to.account_no)

                if transaction.credential == account_from.credential:
                    if account_from.balance >= transaction.amount:
                        cur_balance = account_from.balance - transaction.amount
                        account_from.balance = cur_balance
                    else:
                        return Response({"error" : "Your account balance is low."},
                                        status= status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error" : "Credential does not match."},
                                        status= status.HTTP_400_BAD_REQUEST)
            
            
                cur_balance =  account_to.balance + transaction.amount
                account_to.balance = cur_balance
                transaction.status = 'A'
                transaction.is_approved = True

                account_from.save()
                transaction.save()
                account_to.save()
            else:
                return Response({"error" : "Something Went Wrong."},
                                        status= status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error' : 'Sorry Something Went Wrong!'})

        
        return Response({'msg': 'Your Send MoneyRequest Successfully Approved'},
                        status = status.HTTP_200_OK)
from re import S
import requests

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from config.paginations import PagePagination
from .models import BankOption, BankAccount, Transaction
from apps.accounts.models import Profile
from .permissions import (IsBankAccountOwnerOrManager,
                          IsBankManager)
from .serializers import (BankAccountSerializer,
                          BankAccountCreateSerializer_,
                          BankAccountCreateSerializer,
                          BankAccountUpdateSerializer,
                          AddMoneyRequestSerializer,
                          AddMoneyRequestSerializer_,
                          SendMoneyRequestSerializer,
                          SendMoneyRequestSerializer_,
                          TransactionSerializer)

# Create your views here.
class BankAccountCreateAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BankAccountCreateSerializer_

    def post(self, request):
        acc_obj = BankOption.objects.get(key= 'account_no')
        acc_no = acc_obj.value + 1
        acc_obj.value = acc_no
        acc_obj.save()

        bank_account_data = request.data
        bank_account_data['account_no'] = acc_no

        serializer = BankAccountCreateSerializer(data = bank_account_data)

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
            
            return Response(serializer.data, status= status.HTTP_201_CREATED)

        return Response({'error': 'Something Went wrong.Try again'})



class BankAccountUpdateAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsBankAccountOwnerOrManager]
    serializer_class = BankAccountUpdateSerializer

    def put(self, request, account_no, format=None):
        try:
            account_instance = BankAccount.objects.get(account_no = account_no)
        except:
            return Response({'error':'Bank Account does not exist'}, status = status.HTTP_400_BAD_REQUEST)

        self.check_object_permissions(request, account_instance) 

        serializer = self.serializer_class(
                            instance= account_instance,
                            data = request.data,
                            partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data , status = status.HTTP_200_OK)
    
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
            acc_instance = BankAccount.objects.get(account_no = account_no)
        except:
            return Response({'error':'Bank Account does not exist'}, status = status.HTTP_400_BAD_REQUEST)

        serializer = BankAccountSerializer(acc_instance)
        return Response(serializer.data, status= status.HTTP_200_OK)


class BankAccountListAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated,IsBankManager]
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()
    pagination_class = PagePagination


class AddMoneyToAccountRequestAPI(generics.GenericAPIView):
    serializer_class = AddMoneyRequestSerializer_

    def post(self, request):
        serializer = AddMoneyRequestSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            s = serializer.save()
            return Response({'msg': 'Money Added Request Sent Successfully.',
                            'transaction_id' : s.id},
                            status = status.HTTP_200_OK)
        
        return Response({"error" : "Add Money Request Can't be sent!"})



class SendMoneyToAccountRequestAPI(generics.GenericAPIView):
    serializer_class = SendMoneyRequestSerializer_

    def post(self, request):
        print(request.data)
        serializer = SendMoneyRequestSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            transaction= serializer.save()

            current_site = get_current_site(request).domain
            relative_link = reverse('bank:approve_send_money_request', args=[transaction.id])
            abs_url = 'http://' + str(current_site) + relative_link

            approve_send_money = requests.get(abs_url)

            if approve_send_money.status_code == 200:
                return Response({'msg' : 'Send Money Approved Successfully',
                                 'transaction_id' : transaction.id},
                            status = status.HTTP_200_OK)
        
        return Response({"error" : "Send Money Request Can't be sent!"},
                         status = status.HTTP_400_BAD_REQUEST)



class TransactionSingleAPI(APIView):
    permission_classes = [IsAuthenticated, IsBankManager]
    def get(self,request, transaction_id):
        try:
            transaction = Transaction.objects.get(id = transaction_id)
            serialiazer = TransactionSerializer(transaction)
            return Response(serialiazer.data, status.HTTP_200_OK)
        except:
            return Response({'error': 'Somethimg went wrog!'},
                            status = status.HTTP_400_BAD_REQUEST)



class TransactionListAPI(generics.ListAPIView):
        permission_classes = [IsAuthenticated,IsBankManager]
        queryset = Transaction.objects.all()
        serializer_class = TransactionSerializer
        pagination_class = PagePagination



class TransactionFilterAPI(generics.ListAPIView):
    account_from = BankAccountSerializer
    permission_classes = [IsAuthenticated,IsBankManager]
    queryset = Transaction.objects.all().order_by('-created_at')
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = PagePagination
    filterset_fields = ('id', 'account_from__account_no', 'account_to__account_no','status', 'type',
                        'created_at', 'is_approved', 'approved_by')



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
                return Response({'error' : 'Sorry Something Went Wronggjghjhjhjj!'},
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
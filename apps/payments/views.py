import requests

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from apps.orders.models import Order
from apps.store.models import Store
from apps.payments import serializers

# Create your views here.


class MakePayment(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.MakePaymentSerializer

    def post(self, request):
        data = request.data
        user = request.user

        order = Order.objects.get(id = data['order_id'])
        store = Store.objects.get(id = order.store.id)
        print("==================================")
        print('user::::', request.user)
        print('bank: ', user.profile.bank_account)
        account_from = data['account_from'] if data.get('account_from', '') != '' else user.profile.bank_account

        current_site = get_current_site(request).domain
        relative_link = reverse('bank:send_money_request')
        abs_url = 'http://' + str(current_site) + relative_link

        send_money_request_data = {
                "credential": data['credential'],
                "amount" : data['amount'],
                "account_from" : account_from,
                "account_to" : store.owner.profile.bank_account,
                }

        send_money= None
        # print(type(data['amount']))
        if float(data['amount']) == order.total_price:
            send_money = requests.post(abs_url, data=send_money_request_data)
        else:
            return Response({'error': 'Payment Failure.Amounts dont match.',
                             'order_id': order.id}, status = status.HTTP_400_BAD_REQUEST)         

        if send_money.status_code == 200:
            order.billing_status = 'P'
            order.save()
            return Response({'msg': 'Payment Successful. Track Your Order with Order ID',
                             'order_id': order.id}, status = status.HTTP_200_OK)

        return Response({'error': 'Payment Failure',
                             'order_id': order.id}, status = status.HTTP_400_BAD_REQUEST)                             
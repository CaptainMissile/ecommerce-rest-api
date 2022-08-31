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

        send_money = requests.post(abs_url, data=send_money_request_data)
        print(send_money, "============================")
        if send_money.status_code == 200:
            return Response({'msg': 'Payment Successful. Track Your Order with Order ID',
                             'order_id': order.id}, status = status.HTTP_200_OK)

        return Response({'error': 'Payment Failure',
                             'order_id': order.id}, status = status.HTTP_400_BAD_REQUEST)                             
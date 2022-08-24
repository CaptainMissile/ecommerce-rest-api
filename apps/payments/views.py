import requests

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import views
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order
from apps.store.models import Store
# Create your views here.
class MakePayment(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(request):
        order_id = request.data.order_id
        
        order = Order.objects.get(id = order_id)

        store_id = order.store.id
        store = Store.objects.get(id = store_id)

        if request.data.get('account_from', '') is not '':
            account_from = request.data.account_from
        else:
            account_from = request.user.profile.bank_account

        current_site = get_current_site(request).domain
        relative_link = reverse('orders:send_money')
        abs_url = 'http://' + str(current_site) + relative_link

        send_money_request_data = {
                "credential": request.data.credential,
                "amount" : request.data.amount,
                "account_to" : store.owner.profile.bank_account,
                "account_from" : account_from
                } 

        api_call = requests.post(abs_url, data=send_money_request_data)
        print(api_call.json())

        # return Response({})
        
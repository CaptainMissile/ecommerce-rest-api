from django.urls import path

from .views import MakePayment
app_name = "payments"

urlpatterns = [
    path('make-payment/', MakePayment.as_view(), name="make_payment"),
]

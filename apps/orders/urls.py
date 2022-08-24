from django.urls import path

from .views import PlaceTheOrder

app_name = "orders"

urlpatterns = [
    path('place-the-order/', PlaceTheOrder.as_view(), name= "place_order")
]

from django.urls import path

from .views import (PlaceTheOrder, TrackOrder, TrackOrderList, OrderItemList,
                    ChangeOrderStatus)

app_name = "orders"

urlpatterns = [
    path('place-the-order/', PlaceTheOrder.as_view(), name= "place_order"),
    path('track-orders/', TrackOrderList.as_view(), name= "track_order_list"),
    path('track-orders/<int:order_id>/', TrackOrder.as_view(), name= "track_order"),
    path('change-order-status/<int:order_id>/', ChangeOrderStatus.as_view(), name= "change_order_status"),
    path('order-item-list/<int:order_id>/', OrderItemList.as_view(), name= "order_item_list"),
]

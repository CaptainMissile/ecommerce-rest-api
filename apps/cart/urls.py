from django.urls import path

from .views import (AddAndUpdateToCartAPI,
                    CartFilteredListAPI,
                    DeleteAllCartItemAPI,
                    DeleteSingleCartItemAPI)

app_name = "cart"

urlpatterns = [
    path('list-cart/', CartFilteredListAPI.as_view(), name="add_to_cart"),
    path('add-update-to-cart/', AddAndUpdateToCartAPI.as_view(), name="add_to_cart"),
    path('delete-cart/', DeleteAllCartItemAPI.as_view(), name="delete_all_cart"),
    path('delete-cart/<int:id>', DeleteSingleCartItemAPI.as_view(), name="delete_single_cart"),
]

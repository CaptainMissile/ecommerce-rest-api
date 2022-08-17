from django.urls import path

from .views import BankAccountCreateAPI

app_name = 'bank'

urlpatterns = [
    path('create-account/', BankAccountCreateAPI.as_view(), name='create_account'),
    # path('delete-store/<int:store_id>', StoreDeleteAPI.as_view(), name='delete_store'),
    # path('update-store/<int:store_id>', StoreUpdateAPI.as_view(), name="update-store"),
    # path('single-store/<int:store_id>', StoreSingleAPI.as_view(), name="store-single"),
    # path('list-store/', StoreListAPI.as_view(), name="store-list"),
    # path('filter-store/', StoreFilteredListAPI.as_view(), name="store-filter"),
]

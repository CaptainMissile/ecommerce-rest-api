from django.urls import path

from .views import (StoreCreateAPI, StoreDeleteAPI,StoreUpdateAPI,
                    StoreFilteredListAPI,StoreListAPI,StoreSingleAPI)

app_name = 'store'

urlpatterns = [
    path('create-store/', StoreCreateAPI.as_view(), name='create_store'),
    path('delete-store/<int:id>', StoreDeleteAPI.as_view(), name='delete_store'),
    path('update-store/<int:id>', StoreUpdateAPI.as_view(), name="update-store"),
    path('single-store/<int:id>', StoreSingleAPI.as_view(), name="store-single"),
    path('list-store/', StoreListAPI.as_view(), name="store-list"),
    path('filter-store/', StoreFilteredListAPI.as_view(), name="store-filter"),
]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls', namespace= 'accounts')),
    path('api/store/', include('apps.store.urls', namespace= 'store')),
    path('api/products/', include('apps.products.urls', namespace= 'products')),
    path('api/bank/', include('apps.bank.urls', namespace= 'bank'))
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

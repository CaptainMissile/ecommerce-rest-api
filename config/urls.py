from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Ecommerce & Banking API",
      default_version='alpha',
      description="Build Your Test Ecommerce and Banking Frontend Using our API",
      contact=openapi.Contact(email="sazin.me@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls', namespace= 'accounts')),
    path('api/store/', include('apps.store.urls', namespace= 'store')),
    path('api/products/', include('apps.products.urls', namespace= 'products')),
    path('api/cart/', include('apps.cart.urls', namespace= 'cart')),
    path('api/orders/', include('apps.orders.urls', namespace= 'orders')),
    path('api/payments/', include('apps.payments.urls', namespace= 'payments')),
    path('api/bank/', include('apps.bank.urls', namespace= 'bank')),

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


admin.site.index_title = 'Rest API'
admin.site.site_header = "Ecommerce & Banking Dashboard"
admin.site.site_title= "Admin"
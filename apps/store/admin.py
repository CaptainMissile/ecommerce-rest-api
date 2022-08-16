from django.contrib import admin

from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    class Meta:
        model = Store
        readonly_fields = ('id',)

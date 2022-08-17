from dataclasses import fields
from django.contrib import admin

from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    class Meta:
        model = Store
        fields = ('id', 'name', 'location', 'description')
        readonly_fields= ('id',)

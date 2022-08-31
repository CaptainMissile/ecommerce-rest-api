from django.db import models
from django.conf import settings

# Create your models here.
class Store(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                on_delete=models.SET_NULL)
    name = models.CharField(max_length = 50,  blank=True, null=True)

    location = models.CharField(max_length = 50, blank=True, null=True)
    description = models.CharField(max_length = 50, blank=True, null=True)

    def __str__(self):
        return 'Store: ' + self.name

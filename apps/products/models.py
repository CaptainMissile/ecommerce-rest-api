from django.db import models

from apps.store.models import Store

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class ProductInventory(models.Model):
    store = models.ForeignKey(Store, on_delete= models.CASCADE)
    category= models.ForeignKey(Category, on_delete= models.CASCADE)

    name = models.CharField(max_length=100, blank=True, null=True)
    img = models.ImageField(upload_to='images/', default = "images/default.png")
    desc = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    units = models.IntegerField(default=0)
    units_sold = models.IntegerField(default=0)

    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Product Inventories"
    
    def __str__(self):
        return self.name
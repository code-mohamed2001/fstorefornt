from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from store.admin import ProductAdmin
from tags.models import TagedItem
from store.models import Product
# Register your models here.


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TagedItem

class CustomeProductAdmin(ProductAdmin):
    inlines=[TagInline]

admin.site.unregister(Product)
admin.site.register(Product,CustomeProductAdmin)
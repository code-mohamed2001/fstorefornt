from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .import models


# Register your models here.


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({
                   'collection__id': str(collection.id)
               }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    search_fields = ['title']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update']
    list_per_page = 20

    # To select a specific field in the model we use this part
    # list_select_related=['collction']
    # def collection_title(self,product):
    # return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory == 0:
            return 'None'
        elif product.inventory < 10:
            return 'Low'
        return 'Normal'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} product/s were successfully updated',
            messages.SUCCESS
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'membership', 'number_of_orders']
    list_editable = ['membership']
    list_per_page = 20
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='number_of_orders')
    def number_of_orders(self, customer):
        url = (reverse('admin:store_order_changelist')
               + '?'
               + urlencode({
                   'customer__id': str(customer.id)
               }))
        return format_html('<a href="{}">{}</a>', url, customer.number_of_orders)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            number_of_orders=Count('order')
        )


class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 1
    min_num = 1
    max_num = 5
    readonly_fields = ['unit_price']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    fields = ['payment_status', 'customer']
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    list_editable = ['payment_status']
    list_per_page = 20
    list_select_related = ['customer']

    def customer_name(self, order):
        return order.customer.first_name

from django.contrib import admin
from unfold.admin import ModelAdmin
import admin_thumbnails

from cart.models import Cart

# Register your models here.
class CartAdmin(ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'single_price', 'qty_total_price', ]
    search_fields = ['user__username', 'product__title']
    list_filter = ['user', 'product', 'quantity']
    readonly_fields = ['single_price', 'qty_total_price', ]
admin.site.register(Cart, CartAdmin)
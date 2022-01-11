from django.contrib import admin
from .models import Menu, Customers


# Register your models here.
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('product_ID', 'product_name')


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('customer_ID', 'customer_name')

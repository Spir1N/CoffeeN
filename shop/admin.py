from django.contrib import admin
from shop.models import Customer, Order, OrderItem, Product

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
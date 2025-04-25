from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from shop.models import Customer, Order, Product
from django.db.models import Q
from django.shortcuts import render


class HomePageView(TemplateView):
    template_name = 'home.html'

class CustomersListView(ListView):
    template_name = "customers.html"
    model = Customer
    context_object_name = "list_of_all_customers"

class OrdersListView(ListView):
    template_name = "orders.html"
    model = Order
    context_object_name = "list_of_all_orders"

class OrderDetailView(DetailView):
    template_name = "order_detail.html"
    model = Order
    context_object_name = "order"

class SearchView(ListView):
    template_name = "search.html"
    model = Order
    context_object_name = "list_of_all_orders"
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Order.objects.filter(
            Q(customer__first_name__icontains=query) | 
            Q(customer__last_name__icontains=query)
            ).order_by('order_date').reverse()
    
class Products(ListView):
    template_name = "products/product_list.html"
    model = Product
    context_object_name = "products"



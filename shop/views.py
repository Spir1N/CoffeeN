from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from shop.models import Customer, Order, Product
from django.db.models import Q, F, FloatField, Value
from django.shortcuts import render
from favorites.models import Favorite
from django.db.models.functions import Cast


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


def product_list(request):
    qs = Product.objects.all()

    # --- поисковая строка ---------------------------------------------------
    q = request.GET.get("q", "")
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    # --- собираем фильтры ---------------------------------------------------
    selected_roasts    = request.GET.getlist("roast")
    selected_countries = request.GET.getlist("country")
    selected_densities = request.GET.getlist("density")
    selected_acidities = request.GET.getlist("acidity")

    if selected_roasts:
        qs = qs.filter(roast_level__in=selected_roasts)
    if selected_countries:
        qs = qs.filter(country__in=selected_countries)
    if selected_densities:
        qs = qs.filter(density__in=selected_densities)
    if selected_acidities:
        qs = qs.filter(acidity__in=selected_acidities)

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price:
        qs = qs.filter(price__gte=min_price)
    if max_price:
        qs = qs.filter(price__lte=max_price)

    # --- сортировка ---------------------------------------------------------
    sort_key = request.GET.get("sort", "name")
    if sort_key.startswith("rating"):
        qs = qs.annotate(
            rating_avg_calc=Cast(F("rating_sum"), FloatField()) / F("rating_count")
        )
    qs = qs.order_by(ALLOWED_SORTS.get(sort_key, "name"))

    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = Favorite.objects.filter(user=request.user)\
                                       .values_list("product_id", flat=True)

    context = {
        "products": qs,
        "favorite_ids": favorite_ids,
        "params": request.GET.urlencode(),

        # --- вот эти четыре списка нужны шаблону ---------------------------
        "selected_roasts":    selected_roasts,
        "selected_countries": selected_countries,
        "selected_densities": selected_densities,
        "selected_acidities": selected_acidities,
    }
    return render(request, "products/product_list.html", context)



ALLOWED_SORTS = {
    "price": "price",
    "-price": "-price",
    "name": "name",
    "-name": "-name",
    "new": "-created_at",
    "old": "created_at",
    "rating": "-rating_avg_calc",
}
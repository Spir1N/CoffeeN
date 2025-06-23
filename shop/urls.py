from django.urls import path, include
from .views import HomePageView, CustomersListView, OrdersListView, OrderDetailView, SearchView, Products, product_list
from django. conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('customers', CustomersListView.as_view(), name='customers'),
    path('orders', OrdersListView.as_view(), name='orders'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
    path('search', SearchView.as_view(), name='search'),
    path("products", product_list, name="product_list"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
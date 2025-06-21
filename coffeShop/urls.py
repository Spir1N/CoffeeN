from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('favorites/', include('favorites.urls')),
    path('profile/', include('userprofile.urls', namespace='userprofile')),
    path("reviews/", include(("reviews.urls"), namespace="reviews")),
    path('', include('shop.urls')),
]

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Product
from .models import Favorite

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f'Товар "{product.name}" добавлен в избранное.')
    return redirect(request.META.get('HTTP_REFERER', 'favorites:favorite_list'))

@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Favorite.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f'Товар "{product.name}" удалён из избранного.')
    return redirect(request.META.get('HTTP_REFERER', 'favorites:favorite_list'))

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'favorites/favorite_list.html', {'favorites': favorites})
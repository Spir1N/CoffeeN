from django.shortcuts import render, redirect
from shop.models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from .tasks import order_created
from userprofile.models import Profile

def order_create(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, cart=cart)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            cart.clear()
            order_created.delay(order.id)
            return render(request, 'orders/created.html', {'order': order})
    
    else:
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                initial_data = {
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'email': profile.email,
                    'city': profile.address,  # если адрес = город + улица, скорректируй
                    'room': '',               # можно оставить пустым
                }
            except Profile.DoesNotExist:
                initial_data = {}

        else:
            initial_data = {}

        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'orders/create.html', {
        'cart': cart,
        'form': form
    })

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/list.html', {'orders': orders})
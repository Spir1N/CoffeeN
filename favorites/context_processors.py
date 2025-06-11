from .models import Favorite

def favorite_ids(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
        return {'favorite_ids': list(favorites)}
    return {'favorite_ids': []}
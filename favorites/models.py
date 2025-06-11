from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product  # Импортируем модель товара из твоего приложения

User = get_user_model()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Один товар — одна запись у пользователя

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
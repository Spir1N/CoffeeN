from django.conf import settings
from django.db import models
from shop.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=0
    )
    body    = models.TextField()
    created   = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "author")  # один отзыв на товар от одного пользователя
        ordering = ("-created",)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        old_rating = None
        if not is_new:
            old_rating = Review.objects.filter(pk=self.pk).values_list("rating", flat=True).first()

        super().save(*args, **kwargs)

        # обновляем агрегаты продукта
        diff = self.rating - (old_rating or 0)
        Product.objects.filter(pk=self.product_id).update(
            rating_sum=models.F("rating_sum") + diff,
            rating_count=models.F("rating_count") + (1 if is_new else 0)
        )

    def delete(self, using=None, keep_parents=False):
        Product.objects.filter(pk=self.product_id).update(
            rating_sum=models.F("rating_sum") - self.rating,
            rating_count=models.F("rating_count") - 1
        )
        return super().delete(using, keep_parents)

class Question(models.Model):
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE, related_name="questions")
    author  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body    = models.TextField()
    answer   = models.TextField(blank=True)      # можно добавить модератору возможность отвечать
    created  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)

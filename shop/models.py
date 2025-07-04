from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

class Customer(models.Model):
    customer_id = models.AutoField("ID", primary_key=True)
    email = models.EmailField("E-mail", max_length=256, unique=True)
    first_name = models.CharField("Имя", max_length=256)
    last_name = models.CharField("Фамилия", max_length=256)
    phone_number = models.CharField("Номер телефона", max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)  
    

class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders', verbose_name="Пользователь", null=True)
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    email = models.EmailField("E-mail")
    city = models.CharField("Город", max_length=100)
    postal_code = models.CharField("Почтовый индекс", max_length=20)
    room = models.CharField("Номенр дома и квартира", max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ {self.id}'
    

class Product(models.Model):
    product_id = models.AutoField("ID", primary_key=True)
    name = models.CharField("Название", max_length=256)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=0)
    description = models.TextField("Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    rating_sum = models.PositiveIntegerField(default=0, editable=False)
    rating_count = models.PositiveIntegerField(default=0, editable=False)
    ROAST_CHOICES = [
        ("light",  "Светлая"),
        ("medium", "Средняя"),
        ("dark",   "Тёмная"),
    ]

    roast_level = models.CharField(max_length=6, choices=ROAST_CHOICES, default='medium')

    country = models.CharField(max_length=64, default='Brazil')             # "Brazil", "Ethiopia"…
    density = models.CharField(max_length=8, default='low')              # high / medium / low
    acidity = models.CharField(max_length=8, default='low')

    def __str__(self):
        return f'Товар {self.name}'
    
    @property
    def rating_avg(self):
        if self.rating_count:
            return round(self.rating_sum / self.rating_count, 1)
        
    def get_absolute_url(self):
        return reverse("reviews:product", args=[self.pk])


class OrderItem(models.Model):
    order_item_id = models.AutoField("ID", primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                              related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.order_item_id}'
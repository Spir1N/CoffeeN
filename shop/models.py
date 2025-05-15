from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField("ID", primary_key=True)
    email = models.EmailField("E-mail", max_length=256)
    first_name = models.CharField("First Name", max_length=256)
    last_name = models.CharField("Last Name", max_length=256)
    phone_number = models.CharField("Phone Number", max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)  
    

class Order(models.Model):
    order_id = models.AutoField("ID", primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField("Order Date")
    status = models.SmallIntegerField("Status")
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Заказ № {self.order_id}'
    

class Product(models.Model):
    product_id = models.AutoField("ID", primary_key=True)
    name = models.CharField("Name", max_length=256)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Quantity", default=0)
    description = models.TextField("Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Товар {self.name}'
    

class OrderItem(models.Model):
    order_item_id = models.AutoField("ID", primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Quantity", default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Товар № {self.order_item_id}'
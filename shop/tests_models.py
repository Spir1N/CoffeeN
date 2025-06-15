from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Customer, Order, Product, OrderItem


class CustomerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.customer = Customer.objects.create(
            email="test@example.com",
            first_name="Иван",
            last_name="Петров",
            phone_number="+79991234567"
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.first_name, "Иван")
        self.assertEqual(self.customer.last_name, "Петров")
        self.assertEqual(str(self.customer), "Иван Петров")

    def test_email_unique(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                email="test@example.com",  # Дубликат
                first_name="Дубликат",
                last_name="Тест",
                phone_number="+79997654321"
            )

    def test_phone_field_length(self):
        max_length = self.customer._meta.get_field('phone_number').max_length
        self.assertEqual(max_length, 20)

    def test_auto_timestamps(self):
        from datetime import datetime
        self.assertIsNotNone(self.customer.created_at)
        self.assertIsNotNone(self.customer.updated_at)
        self.assertIsInstance(self.customer.created_at, datetime)
        self.assertIsInstance(self.customer.updated_at, datetime)


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(
            name="Coffee №5",
            price=250.50,
            quantity=100,
            description="Кофе с тёмной обжаркой"
        )

    def test_product_creation(self):
        self.assertEqual(self.product.price, 250.50)
        self.assertEqual(self.product.quantity, 100)
        self.assertEqual(str(self.product), "Товар Coffee №5")

    def test_price_decimal_places(self):
        decimal_places = self.product._meta.get_field('price').decimal_places
        self.assertEqual(decimal_places, 2)

    def test_quantity_default(self):
        product = Product.objects.create(
            name="Черничный вулкан",
            price=300.00,
            description="Взрывная черника"
        )
        self.assertEqual(product.quantity, 0)

    def test_product_str_method(self):
        self.assertEqual(str(self.product), f"Товар {self.product.name}")


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username='testuser',
            email='user@example.com',
            password='testpass123'
        )
        
        cls.order = Order.objects.create(
            user=cls.user,
            first_name="Анна",
            last_name="Сидорова",
            email="anna@example.com",
            city="Москва",
            postal_code="123456",
            room="ул. Пушкина, д.10, кв.5",
            paid=True,
            total_amount=1000.00
        )

    def test_order_creation(self):
        self.assertEqual(self.order.first_name, "Анна")
        self.assertEqual(self.order.city, "Москва")
        self.assertTrue(self.order.paid)
        self.assertEqual(str(self.order), f"Заказ {self.order.pk}")

    def test_order_user_relation(self):
        self.assertEqual(self.order.user.email, 'user@example.com')
        self.assertEqual(self.order.user, self.user)


class OrderItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser2',
            email='user2@example.com',
            password='testpass123'
        )
        
        cls.product = Product.objects.create(
            name="Спящий дракон",
            price=350.00,
            quantity=50,
            description="Огненно тихий кофе"
        )
        
        cls.order = Order.objects.create(
            user=user,
            first_name="Тест",
            last_name="Заказ",
            email="test@example.com",
            city="Москва",
            postal_code="123123",
            room="ул. Тестовая, д.1"
        )
        
        cls.order_item = OrderItem.objects.create(
            order=cls.order,
            product=cls.product,
            price=cls.product.price,
            quantity=2
        )

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.price, 350.00)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(str(self.order_item), str(self.order_item.order_item_id))

    def test_order_item_relations(self):
        self.assertEqual(self.order_item.product.name, "Спящий дракон")
        self.assertEqual(self.order_item.order.email, "test@example.com")



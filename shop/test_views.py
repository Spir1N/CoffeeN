from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from shop.models import Customer, Order, Product
from shop.views import *

class HomePageViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class CustomersListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Customer.objects.create(
            email="test1@example.com",
            first_name="Иван",
            last_name="Петров",
            phone_number="+79991234567"
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/customers')  # Без слеша в конце
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('customers'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('customers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers.html')

    def test_lists_all_customers(self):
        response = self.client.get(reverse('customers'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['list_of_all_customers']), 1)


class OrdersListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username='testuser',
            email='user@example.com',
            password='testpass123'
        )
        
        Order.objects.create(
            user=cls.user,
            first_name="Тест",
            last_name="Заказ",
            email="test@example.com",
            city="Москва",
            postal_code="123456",
            room="ул. Тестовая, д.1",
            paid=True,
            total_amount=1000.00
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/orders')  # Без слеша в конце
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders.html')

    def test_lists_all_orders(self):
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['list_of_all_orders']), 1)


class OrderDetailViewTest(TestCase):
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
            first_name="Тест",
            last_name="Заказ",
            email="test@example.com",
            city="Москва",
            postal_code="123456",
            room="ул. Тестовая, д.1",
            paid=True,
            total_amount=1000.00
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/orders/{self.order.pk}')  # Без слеша в конце
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('order-detail', args=[self.order.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('order-detail', args=[self.order.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_detail.html')

    def test_view_returns_correct_order(self):
        response = self.client.get(reverse('order-detail', args=[self.order.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['order'], self.order)


class OrderDetailViewTest(TestCase):
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
            first_name="Тест",
            last_name="Заказ",
            email="test@example.com",
            city="Москва",
            postal_code="123456",
            room="ул. Тестовая, д.1",
            paid=True,
            total_amount=1000.00
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/orders/{self.order.pk}')  # Без слеша в конце
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('order-detail', args=[self.order.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('order-detail', args=[self.order.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_detail.html')

    def test_view_returns_correct_order(self):
        response = self.client.get(reverse('order-detail', args=[self.order.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['order'], self.order)

class SearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username='testuser',
            email='user@example.com',
            password='testpass123'
        )
        
        Order.objects.create(
            user=cls.user,
            first_name="Иван",
            last_name="Петров",
            email="ivan@example.com",
            city="Москва",
            postal_code="123456",
            room="ул. Пушкина, д.1",
            paid=True,
            total_amount=1000.00
        )


class ProductsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name="Эспрессо",
            price=250.50,
            quantity=100,
            description="Крепкий черный кофе"
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/products')  # Без слеша в конце
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')

    def test_lists_all_products(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 1)


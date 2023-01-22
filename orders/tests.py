from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from cart.cart import Cart
from products.models import Product, Category
from .models import OrderItem, Order


class OrderDetailTest(TestCase):
    def setUp(self):
        product = Product.objects.create(
            category=Category.objects.create(fa_title='title', en_title='title'),
            title='product_title',
            description='sample description',
            price=19.9,
            image='static/images/client1.png'
        )
        self.product = product

        user = get_user_model().objects.create_user(
            username='sample',
            email='testing@gmail.com',
            password='password123456789',
        )
        self.user = user

        self.client.post('/en/accounts/login/', {'password': 'password123456789',
                                                 'login': 'testing@gmail.com'}, follow=True)

    def test_order_detail_page_by_url(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                         {'quantity': 1, 'inplace': False}, follow=True)
        response = self.client.get('/en/order/create/')
        self.assertEqual(response.status_code, 200)

    def test_order_detail_page_reverse(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                         {'quantity': 1, 'inplace': False}, follow=True)
        response = self.client.get(reverse('order_create'))
        self.assertEqual(response.status_code, 200)

    def test_order_detail_page_content(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                         {'quantity': 1, 'inplace': False}, follow=True)
        response = self.client.get(reverse('order_create'))
        self.assertContains(response, 'product_title')
        self.assertContains(response, 'Order Create')
        self.assertContains(response, self.product.title)
        self.assertContains(response, self.product.price)

    def test_order_detail_page_template_used(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                         {'quantity': 1, 'inplace': False}, follow=True)

        response = self.client.get(reverse('order_create'))
        self.assertTemplateUsed(response, 'orders/order_create.html')

    def test_order_create_view_post(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                         {'quantity': 1, 'inplace': False}, follow=True)

        response = self.client.post(reverse('order_create'), {'first_name': 'ali',
                                                              'last_name': 'alavi',
                                                              'address': 'sample_address',
                                                              'phone_number': '091212121',
                                                              'order_notes': 'sample_note'}, follow=True)

        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Your Order has been submitted')

        self.assertEqual(Order.objects.all()[0].user, self.user)
        self.assertEqual(Order.objects.all()[0].first_name, 'ali')
        self.assertEqual(Order.objects.all()[0].address, 'sample_address')
        self.assertEqual(OrderItem.objects.all()[0].product, self.product)
        self.assertEqual(OrderItem.objects.all()[0].order, Order.objects.all()[0])

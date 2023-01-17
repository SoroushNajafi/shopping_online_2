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
        )
        self.product = product

    def test_order_detail_page_by_url(self):
        user = get_user_model().objects.create_user(
            username='sample',
            email='testing@gmail.com',
            password='password123456789',
        )

        self.client.post('/en/accounts/login/', {'password': 'password123456789',
                                                 'login': 'testing@gmail.com'})
        request = self.client.get('/en/').wsgi_request
        cart = Cart(request)
        self.cart = cart
        self.cart.add(product=self.product)
        response = self.client.get('/en/order/create/')
        self.assertEqual(response.status_code, 200)

    # def test_order_detail_page_reverse(self):
    #     response = self.client.get(reverse('order_create'))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_order_detail_page_content(self):
    #     response = self.client.get(reverse('order_create'))
    #     self.assertContains(response, 'product_title')
    #     self.assertContains(response, 'ORDER CREATE')
    #
    # def test_order_detail_page_template_used(self):
    #     response = self.client.get(reverse('order_create'))
    #     self.assertTemplateUsed(response, 'orders/order_create.html')


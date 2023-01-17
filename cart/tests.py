from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .cart import Cart
from products.models import Product, Category


class CartDetailView(TestCase):
    def setUp(self):
        category = Category.objects.create(
            en_title='sample',
            fa_title='sample',
        )
        product = Product.objects.create(
            category=category,
            title='product_title',
            description='sample description',
            price=19.9,
        )
        self.product = product
        request = self.client.get('/en/').wsgi_request
        cart = Cart(request)
        self.cart = cart
        self.cart.add(product=product)

    def test_cart_detail_page_url(self):
        response = self.client.get('/en/cart/')
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_page_reverse(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_page_content(self):

        response = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response, 'Cart Detail')
        self.assertEqual(len(self.cart), 1)

    def test_cart_detail_page_template_used(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertTemplateUsed(response, 'cart/cart_detail.html')


class AddToCartTest(TestCase):
    def setUp(self):
        category = Category.objects.create(
            en_title='sample',
            fa_title='sample',
        )
        product = Product.objects.create(
            category=category,
            title='product_title',
            description='sample description',
            price=19.9,
        )
        self.product = product

        # self.cart.add(product=product)

    def test_add_to_cart_url(self):
        request = self.client.get('/en/').wsgi_request
        cart = Cart(request)
        response = self.client.post(f'/en/cart/add/{self.product.id}/')
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(len(cart), 1)

    def test_add_to_cart_reverse(self):
        request = self.client.get('/en/').wsgi_request
        cart = Cart(request)
        response = self.client.post(reverse('cart:add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(len(cart), 1)


class RemoveFromCartTest(TestCase):

    def setUp(self):
        category = Category.objects.create(
            en_title='sample',
            fa_title='sample',
        )
        product = Product.objects.create(
            category=category,
            title='product_title',
            description='sample description',
            price=19.9,
        )
        self.product = product
        request = self.client.get('/en/').wsgi_request
        cart = Cart(request)
        self.cart = cart
        self.cart.add(product=product)

    def test_remove_from_cart_url(self):

        response = self.client.get(f'/en/cart/remove/{self.product.id}/')
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(len(self.cart), 0)

        response1 = self.client.get(reverse('cart:cart_detail'))
        self.assertNotContains(response1, self.product.title)

    def test_remove_from_cart_reverse(self):
        response = self.client.get(reverse('cart:remove_from_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)


class ClearCartTest(TestCase):

    def setUp(self):
        category = Category.objects.create(
            en_title='sample',
            fa_title='sample',
        )
        product = Product.objects.create(
            category=category,
            title='product_title',
            description='sample description',
            price=19.9,
        )
        self.product = product
        request = self.client.get('/en/').wsgi_request
        cart = Cart(request)
        self.cart = cart
        self.cart.add(product=product)

    def test_clear_cart_by_url(self):
        response = self.client.get('/en/cart/clear/')
        self.assertEqual(response.status_code, 302)

    def test_clear_cart_reverse(self):
        response = self.client.get(reverse('cart:cart_clear'))
        self.assertEqual(response.status_code, 302)


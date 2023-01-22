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

    def test_cart_detail_page_url(self):

        self.client.post(f'/en/cart/add/{self.product.id}/', {'quantity': 1, 'inplace': False}, follow=True)

        response = self.client.get('/en/cart/')
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_page_reverse(self):
        self.client.post(f'/en/cart/add/{self.product.id}/', {'quantity': 1, 'inplace': False}, follow=True)

        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_page_content(self):
        response0 = self.client.post(f'/en/cart/add/{self.product.id}/', {'quantity': 1, 'inplace': False}, follow=True)
        request = response0.wsgi_request
        cart = Cart(request)
        self.assertEqual(len(cart), 1)

        response = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response, 'Cart Detail')
        self.assertContains(response, self.product.title)
        self.assertContains(response, self.product.price)

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

    def test_add_to_cart_url(self):
        response = self.client.post(f'/en/cart/add/{self.product.id}/', {'quantity': 1, 'inplace': False}, follow=True)
        request = response.wsgi_request
        self.assertEqual(len(Cart(request)), 1)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Product successfully added to Cart')
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_reverse(self):
        response = self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                                    {'quantity': 1, 'inplace': False}, follow=True)

        request = response.wsgi_request
        self.assertEqual(len(Cart(request)), 1)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Product successfully added to Cart')
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_content(self):
        response = self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                                    {'quantity': 1, 'inplace': False}, follow=True)

        self.assertContains(response, 'product_title')
        self.assertContains(response, 19.9)


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

    def test_remove_from_cart_url(self):

        self.client.post(f'/en/cart/add/{self.product.id}/', {'quantity': 1, 'inplace': False}, follow=True)

        response = self.client.get(f'/en/cart/remove/{self.product.id}/', follow=True)
        request = response.wsgi_request
        cart = Cart(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(cart), 0)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Product successfully removed from Cart')

    def test_remove_from_cart_reverse(self):
        self.client.post(f'/en/cart/add/{self.product.id}/', {'quantity': 1, 'inplace': False}, follow=True)

        response = self.client.get(reverse('cart:remove_from_cart', args=[self.product.id]), follow=True)
        request = response.wsgi_request
        cart = Cart(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(cart), 0)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Product successfully removed from Cart')

    def test_remove_from_cart_content(self):

        self.client.post(f'/en/cart/add/{self.product.id}/', {'quantity': 1, 'inplace': False}, follow=True)

        response = self.client.get(reverse('cart:remove_from_cart', args=[self.product.id]), follow=True)

        self.assertNotContains(response, 'product_title')


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

    def test_clear_cart_by_url(self):
        self.client.post(f'/en/cart/add/{self.product.id}/', {'quantity': 1, 'inplace': False}, follow=True)

        response = self.client.get('/en/cart/clear/', follow=True)
        request = response.wsgi_request
        cart = Cart(request)
        self.assertEqual(len(cart), 0)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'cart is now cleared')
        self.assertEqual(response.status_code, 200)

    def test_clear_cart_reverse(self):
        self.client.post(f'/en/cart/add/{self.product.id}/', {'quantity': 1, 'inplace': False}, follow=True)

        response = self.client.get(reverse('cart:cart_clear'), follow=True)
        request = response.wsgi_request
        cart = Cart(request)
        self.assertEqual(len(cart), 0)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'cart is now cleared')
        self.assertEqual(response.status_code, 200)


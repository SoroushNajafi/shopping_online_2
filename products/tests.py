from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Product, Category, Comment


class ProductListPageTest(TestCase):
    def setUp(self):
        product = Product.objects.create(
            category=Category.objects.create(en_title='title', fa_title='title'),
            title='product_title',
            description='sample_description',
            price=19.99,
        )
        self.product = product

    def test_product_list_page_url(self):
        response = self.client.get('/en/products/')
        self.assertEqual(response.status_code, 200)

    def test_product_list_page_reverse(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_page_content(self):
        response = self.client.get(reverse('product_list'))
        self.assertContains(response, 'product_title')
        self.assertContains(response, 'Products')

    def test_product_list_page_template_used(self):
        response = self.client.get(reverse('product_list'))
        self.assertTemplateUsed(response, 'products/product_list.html')


class ProductDetailPageTest(TestCase):
    def setUp(self):
        product = Product.objects.create(
            category=Category.objects.create(en_title='title', fa_title='title'),
            title='product_title',
            description='sample_description',
            price=19.99,
            image='static/images/client1.png'
        )
        self.product = product

    def test_product_detail_page_url(self):
        response = self.client.get(f'/en/products/{self.product.id}/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_page_reverse(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_page_content(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertContains(response, 'Product Detail')
        self.assertContains(response, 'product_title')

    def test_product_detail_page_template_used(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertTemplateUsed(response, 'products/product_detail.html')


class CategoryListPageTest(TestCase):
    def setUp(self):
        product = Product.objects.create(
            category=Category.objects.create(en_title='title', fa_title='title'),
            title='product_title',
            description='sample_description',
            price=19.99,
            image='static/images/client1.png'
        )
        self.product = product

    def test_category_list_page_url(self):
        response = self.client.get('/en/products/category/')
        self.assertEqual(response.status_code, 200)

    def test_category_list_page_reverse(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)

    def test_category_list_page_content(self):
        response = self.client.get(reverse('category_list'))
        self.assertContains(response, 'title')
        self.assertContains(response, 'Categories')

    def test_category_list_page_template_used(self):
        response = self.client.get(reverse('category_list'))
        self.assertTemplateUsed(response, 'products/categories_list.html')


class ProductsByCategoryPageTest(TestCase):
    def setUp(self):
        product = Product.objects.create(
            category=Category.objects.create(en_title='title', fa_title='title'),
            title='product_title',
            description='sample_description',
            price=19.99,
            image='static/images/client1.png'
        )
        self.product = product

    def test_products_by_category_page_url(self):
        response = self.client.get(f'/en/products/category/{self.product.category.id}/')
        self.assertEqual(response.status_code, 200)

    def test_products_by_category_page_reverse(self):
        response = self.client.get(reverse('products_by_category', args=[self.product.category.id]))
        self.assertEqual(response.status_code, 200)

    def test_products_by_category_page_content(self):
        response = self.client.get(reverse('products_by_category', args=[self.product.category.id]))
        self.assertContains(response, 'Products by Category')
        self.assertContains(response, self.product.category.en_title)
        self.assertContains(response, self.product.title)

    def test_products_by_category_page_template_used(self):
        response = self.client.get(reverse('products_by_category', args=[self.product.category.id]))
        self.assertTemplateUsed(response, 'products/products_by_category.html')


class CommentCreateViewTest(TestCase):
    def setUp(self):
        product = Product.objects.create(
            category=Category.objects.create(en_title='title', fa_title='title'),
            title='product_title',
            description='sample_description',
            price=19.99,
            image='static/images/client1.png'
        )
        self.product = product
        user = get_user_model().objects.create_user(
            username='sample',
            email='testing@gmail.com',
            password='password123456789',
        )

        response = self.client.post('/en/accounts/login/', {'password': 'password123456789',
                                                            'login': 'testing@gmail.com'})

    def test_comment_create_view_url(self):
        response = self.client.post(f'/en/products/comment/{self.product.id}/', {'body': 'sample_body',
                                                                                 'stars': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_create_view_reverse(self):
        response = self.client.post(reverse('comment_create', args=[self.product.id]), {'body': 'sample_body',
                                                                                        'stars': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_create_view_content(self):
        self.client.post(reverse('comment_create', args=[self.product.id]), {'body': 'sample_body',
                                                                             'stars': '1'})
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertContains(response, 'sample_body')


class CommentDeleteViewTest(TestCase):
    def setUp(self):
        product = Product.objects.create(
            category=Category.objects.create(en_title='title', fa_title='title'),
            title='product_title',
            description='sample_description',
            price=19.99,
            image='static/images/client1.png'
        )
        self.product = product

        get_user_model().objects.create_user(
            username='sample',
            email='testing@gmail.com',
            password='password123456789',
        )

        self.client.post('/en/accounts/login/', {'password': 'password123456789',
                                                 'login': 'testing@gmail.com'})

        self.client.post(f'/en/products/comment/{self.product.id}/', {'body': 'sample_body',
                                                                      'stars': '1'})
        comment = Comment.objects.all()[0]
        self.comment = comment

    def test_comment_delete_view_by_url(self):
        response = self.client.post(f'/en/products/comment/delete/{self.comment.id}/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_delete_view_by_reverse(self):
        response = self.client.post(reverse('comment_delete', args=[self.comment.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_delete_view_by_content(self):
        self.client.post(reverse('comment_delete', args=[self.comment.id]))
        response = self.client.get(reverse('product_detail', args=[self.product.id]))

        self.assertNotContains(response, 'sample_body')

    def test_comment_delete_view_by_template_used(self):
        response = self.client.get(reverse('comment_delete', args=[self.comment.id]))
        self.assertTemplateUsed(response, 'products/comment_delete.html')
        self.assertEqual(response.status_code, 200)


class CommentUpdateViewTest(TestCase):
    def setUp(self):
        product = Product.objects.create(
            category=Category.objects.create(en_title='title', fa_title='title'),
            title='product_title',
            description='sample_description',
            price=19.99,
            image='static/images/client1.png'
        )
        self.product = product

        get_user_model().objects.create_user(
            username='sample',
            email='testing@gmail.com',
            password='password123456789',
        )

        self.client.post('/en/accounts/login/', {'password': 'password123456789',
                                                 'login': 'testing@gmail.com'})

        self.client.post(f'/en/products/comment/{self.product.id}/', {'body': 'sample_body',
                                                                      'stars': '1'})
        comment = Comment.objects.all()[0]
        self.comment = comment

    def test_comment_update_view_url(self):
        response = self.client.post(f'/en/products/comment/update/{self.comment.id}/', {'body': 'update_sample',
                                                                                        'stars': '2'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.all()[0].body, 'update_sample')

    def test_comment_update_view_reverse(self):
        response = self.client.post(reverse('comment_update', args=[self.comment.id]), {'body': 'update_sample',
                                                                                        'stars': '2'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.all()[0].body, 'update_sample')
        self.assertEqual(Comment.objects.all()[0].stars, '2')

    def test_comment_update_view_template_used(self):
        response = self.client.get(reverse('comment_update', args=[self.comment.id]))
        self.assertTemplateUsed(response, 'products/comment_update.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Comment')


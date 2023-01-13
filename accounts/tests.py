from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class LoginPageTest(TestCase):

    def test_login_page_by_url(self):
        response = self.client.get('/en/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_reverse(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_content(self):
        response = self.client.get(reverse('account_login'))
        self.assertContains(response, 'Login')

    def test_login_page_template_used(self):
        response = self.client.get(reverse('account_login'))
        self.assertTemplateUsed(response, 'account/login.html')

    def test_login_redirect(self):
        user = get_user_model().objects.create_user(
            username='sample',
            email='testing@gmail.com',
            password='password123456789',
        )

        response = self.client.post('/en/accounts/login/', {'password': 'password123456789',
                                                            'login': 'testing@gmail.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))


class SignupPageTest(TestCase):

    def test_signup_page_url(self):
        response = self.client.get('/en/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page_reverse(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_content(self):
        response = self.client.get(reverse('account_signup'))
        self.assertContains(response, 'Signup')

    def test_signup_page_template_used(self):
        response = self.client.get(reverse('account_signup'))
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_signup_redirect(self):
        response = self.client.post('/en/accounts/signup/', {'email': 'sample_test@gmail.com',
                                                             'password1': 'pass1234sample',
                                                             'password2': 'pass1234sample', })

        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].email, 'sample_test@gmail.com')
        self.assertEqual(get_user_model().objects.all()[0].username, 'sample_test')

        self.assertRedirects(response, reverse('home'))


class LogoutPageTest(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user(
            username='sample',
            email='testing@gmail.com',
            password='password123456789',
        )
        self.client.post('/en/accounts/login/', {'password': 'password123456789',
                                                 'login': 'testing@gmail.com'})

    def test_logout_page_by_url(self):
        response = self.client.get('/en/accounts/logout/')
        self.assertEqual(response.status_code, 200)

    def test_logout_page_reverse(self):
        response = self.client.get(reverse('account_logout'))
        self.assertEqual(response.status_code, 200)

    def test_logout_page_content(self):
        response = self.client.get(reverse('account_logout'))
        self.assertContains(response, 'Logout')

    def test_logout_page_template_used(self):
        response = self.client.get(reverse('account_logout'))
        self.assertTemplateUsed(response, 'account/logout.html')

    def test_logout_redirect(self):
        response = self.client.post('/en/accounts/logout/')

        self.assertRedirects(response, reverse('home'))

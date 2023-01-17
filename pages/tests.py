from django.test import TestCase
from django.shortcuts import reverse

from .models import Contact


class HomePageTest(TestCase):
    def test_home_page_url(self):
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_url_reverse(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Home Page')

    def test_home_page_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'pages/home.html')


class AboutUsPageTest(TestCase):

    def test_about_us_page_url(self):
        response = self.client.get('/en/aboutus/')
        self.assertEqual(response.status_code, 200)

    def test_about_us_page_url_reverse(self):
        response = self.client.get(reverse('aboutus'))
        self.assertEqual(response.status_code, 200)

    def test_about_us_page_content(self):
        response = self.client.get(reverse('aboutus'))
        self.assertContains(response, 'About Us Page')

    def test_about_us_page_template_used(self):
        response = self.client.get(reverse('aboutus'))
        self.assertTemplateUsed(response, 'pages/aboutus.html')


class ContactUsPageTest(TestCase):
    def test_contact_us_page_url(self):
        response = self.client.get('/en/contactus/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'contact us')

    def test_contact_us_page_reverse(self):
        response = self.client.get(reverse('contactus'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'contact us')

    def test_contact_us_page_template_used(self):
        response = self.client.get(reverse('contactus'))
        self.assertTemplateUsed(response, 'pages/contactus.html')

    def test_contact_us_page_post(self):
        response = self.client.post('/en/contactus/', {'name': 'sample_name',
                                                       'email': 'sample_email@gmail.com',
                                                       'message': 'sample_message',
                                                       })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.all()[0].name, 'sample_name')
        self.assertEqual(Contact.objects.all()[0].email, 'sample_email@gmail.com')


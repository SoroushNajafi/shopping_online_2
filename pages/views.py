from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from .froms import ContactUsForm


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutUsPageView(TemplateView):
    template_name = 'pages/aboutus.html'


# class ContactUsPageView(TemplateView):
#     template_name = 'pages/contactus.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['contact_us_form'] = ContactUsForm()
#         return context


def contact_us_view(request):
    if request.method == 'GET':
        return render(request, 'pages/contactus.html', {'contact_us_form': ContactUsForm()})
    else:

        contact_us_form = ContactUsForm(request.POST)

        if contact_us_form.is_valid():
            cleaned_data = contact_us_form.cleaned_data
            sent_name = cleaned_data['name']
            sent_email = cleaned_data['email']
            send_mail(
                _('Thank you for contacting us'),
                _(f'Hi {sent_name}, you have sent a message to our team, we will reach back to you soon, :-)'),
                None,
                [sent_email],
                fail_silently=False,
            )
            messages.success(request, _('Your message is sent successfully.'))
            contact_us_form.save()
            return redirect('home')

        form_errors = contact_us_form.errors
        return render(request, 'pages/contactus.html', {'form_errors': form_errors})

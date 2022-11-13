from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('aboutus/', views.AboutUsPageView.as_view(), name='aboutus'),
    # path('contactus/', views.ContactUsPageView.as_view(), name='contactus'),
    path('contactus/', views.contact_us_view, name='contactus'),
]

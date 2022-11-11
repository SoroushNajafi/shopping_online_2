from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', )


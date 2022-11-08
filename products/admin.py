from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from .models import Product, Comment, Category


class CommentsInline(admin.TabularInline):
    model = Comment
    fields = ['author', 'body', 'stars', 'active']
    extra = 1


@admin.register(Product)
class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'active', 'datetime_created']

    inlines = [CommentsInline, ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'author', 'stars', 'active', 'datetime_created', ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category', ]

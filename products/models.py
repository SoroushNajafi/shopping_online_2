from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.utils.translation import get_language


class Category(models.Model):

    en_title = models.CharField(max_length=30, null=True)
    fa_title = models.CharField(max_length=30, null=True)
    cover = models.ImageField(upload_to='category/category_cover', blank=True)

    def get_name(self):
        current_lang = get_language()
        if current_lang == 'en':
            return self.en_title
        else:
            return self.fa_title

    def __str__(self):
        return self.en_title

    def get_absolute_url(self):
        return reverse('products_by_category', args=[self.id])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)
    title = models.CharField(max_length=200)
    description = RichTextField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product/product_cover/', blank=True)

    datetime_created = models.DateTimeField(default=timezone.now)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id])


class ActiveCommentsManager(models.Manager):
    def get_queryset(self):
        super(ActiveCommentsManager, self).get_queryset().filter(active=True)


class Comment(models.Model):

    PRODUCT_STARS = [
        ('1', _('Very Poor')),
        ('2', _('Poor')),
        ('3', _('Normal')),
        ('4', _('Good')),
        ('5', _('Perfect')),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('comment author'),
    )
    body = models.TextField(verbose_name=_('comment text'))
    stars = models.CharField(verbose_name=_('your score to this product'), max_length=10, choices=PRODUCT_STARS)
    active = models.BooleanField(verbose_name=_('active'), default=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-datetime_created',)

    #manager
    objects = models.Manager()
    active_comments_manager = ActiveCommentsManager()

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.product.id])

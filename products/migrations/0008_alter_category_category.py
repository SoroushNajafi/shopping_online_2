# Generated by Django 4.1.2 on 2022-11-06 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_category_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(choices=[('white', 'White Chocolate'), ('dark', 'Dark Chocolate'), ('nut', 'Nuts Chocolate')], max_length=30, null=True),
        ),
    ]
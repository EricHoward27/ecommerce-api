# Generated by Django 3.0 on 2021-04-18 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='countInStock',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='numReviews',
        ),
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
    ]
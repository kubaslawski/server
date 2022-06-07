# Generated by Django 4.0.5 on 2022-06-07 11:32

import amazon.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0002_customuser_address_customuser_is_seller_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='photo',
            field=models.FileField(default='dsa', upload_to=amazon.models.user_directory_path),
            preserve_default=False,
        ),
    ]

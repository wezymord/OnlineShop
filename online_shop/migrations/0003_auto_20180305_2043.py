# Generated by Django 2.0.2 on 2018-03-05 20:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0002_auto_20180305_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_urls', models.TextField(null=True, validators=[django.core.validators.URLValidator()])),
            ],
        ),
        migrations.RemoveField(
            model_name='products',
            name='image_urls',
        ),
    ]

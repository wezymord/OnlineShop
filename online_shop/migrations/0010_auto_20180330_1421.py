# Generated by Django 2.0.3 on 2018-03-30 14:21

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0009_auto_20180330_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
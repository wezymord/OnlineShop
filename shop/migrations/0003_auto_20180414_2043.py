# Generated by Django 2.0.4 on 2018-04-14 20:43

from django.db import migrations, models
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20180414_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address2',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='company',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128),
        ),
    ]

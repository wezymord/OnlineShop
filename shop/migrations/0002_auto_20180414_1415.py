# Generated by Django 2.0.4 on 2018-04-14 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address2',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='company',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
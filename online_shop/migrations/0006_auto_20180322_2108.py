# Generated by Django 2.0.3 on 2018-03-22 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0005_auto_20180322_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address1',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address2',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='postal_code',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
from django.db import models


class Products(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    quentity = models.IntegerField()
    description = models.CharField(max_length=256)


class Photos(models.Model):
    photos = models.ForeignKey(Products, on_delete=models.CASCADE)


class Users(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=15)          # validation
    e_mail = models.CharField(max_length=64)


class Orders(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products)
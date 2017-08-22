from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField(max_length=100)
    wieght = models.IntegerField(max_length=32)
    price  = models.IntegerField(max_length=32)
    cost = models.IntegerField(max_length=32)
    category = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

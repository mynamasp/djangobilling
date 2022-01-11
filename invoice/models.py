from django.db import models


# Create your models here.
class Menu(models.Model):
    product_ID = models.CharField(max_length=5)
    product_name = models.CharField(max_length=50)
    product_rate_1 = models.FloatField(default=0)
    product_rate_2 = models.FloatField(default=0)
    product_rate_3 = models.FloatField(default=0)


class Customers(models.Model):
    customer_ID = models.CharField(max_length=8)
    customer_name = models.CharField(max_length=50)
    customer_phone_no = models.IntegerField()



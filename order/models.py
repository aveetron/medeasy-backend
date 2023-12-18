from django.db import models
from user.models import MedEasyBaseModel
from product.models import Product


class Order(MedEasyBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
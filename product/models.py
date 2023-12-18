from django.db import models
from user.models import MedEasyBaseModel


class Product(MedEasyBaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Review(MedEasyBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    narrative = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.product.name + "---" + self.narrative


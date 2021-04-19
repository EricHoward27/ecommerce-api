from django.db import models
from django.contrib.auth import get_user_model

#Create Product Model
class Product(models.Model):
    """Class Model for Product"""
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # name have max char length set to 100 and set null to true, and blank to true if user keeps empty
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
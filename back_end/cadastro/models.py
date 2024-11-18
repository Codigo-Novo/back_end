from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

class Institution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    long = models.DecimalField(max_digits=22,decimal_places=16)
    lat = models.DecimalField(max_digits=22,decimal_places=16)
    category = models.ManyToManyField(Category)

class Donation(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    institution = models.ManyToManyField(Institution)

class DonatedBy(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
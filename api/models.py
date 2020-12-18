from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Number(models.Model):
    phone = models.CharField(max_length=12, unique=True)
    spam = models.BooleanField(default=False)

    def __str__(self):
        return self.phone


class Contact(models.Model):
    contactof = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.ForeignKey(Number, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

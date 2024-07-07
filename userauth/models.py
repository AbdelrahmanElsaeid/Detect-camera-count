from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
# Create your models here.






class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    organization = models.CharField(max_length=255)

    
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    

class BillingInfo(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE, related_name='billing_user')
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postal = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    vat_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

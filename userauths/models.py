from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
    
class ContactUs(models.Model):
    
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    
    class Meta:
        verbose_name = "Liên hệ"
        verbose_name_plural = "Contact"
    
    def __str__(self):
        return self.full_name

    

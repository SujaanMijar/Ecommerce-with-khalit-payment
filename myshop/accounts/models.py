from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone=models.CharField(max_length=100)
    street_address=models.CharField(max_length=100)
class Profile(models.Model):
    user=models.OneToOneField(CustomUser,related_name='profile',on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='profile_image')
    bio=models.TextField()
    dob=models.DateField(null=True)
    date=models.DateTimeField(auto_now=True)
from django.db import models
from core.models import Order
# Create your models here.
class Transaction(models.Model):
   order=models.ForeignKey(Order,on_delete=models.CASCADE)
   transaction_id=models.CharField(max_length=200)
   user=models.CharField(max_length=200)
   amount=models.CharField(max_length=200)
   date=models.DateTimeField(auto_now=True) 
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from accounts.models import CustomUser
# Create your models here.
class offerproduct(models.Model):
    title=models.CharField(max_length=100)
    desc=models.TextField()
    price=models.DecimalField(max_digits=9,decimal_places=2)
    image=models.ImageField(upload_to='offer_product')
class Category(models.Model):
    title=models.CharField(max_length=200)
    
    def _str_(self):
        return self.title
class Brands(models.Model):
    title=models.CharField(max_length=200)
    
    def _str_(self):
        return self.title
    
class SubCategory(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)

    def _str_(self):
        return self.title
    
class Product(models.Model):
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory=models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brands=models.ForeignKey(Brands,on_delete=models.CASCADE,null=True)
    desc = CKEditor5Field('Text', config_name='extends')
    image=models.ImageField(upload_to="product_image")
    image2=models.ImageField(upload_to="product_image")
    image3=models.ImageField(upload_to="product_image")
    mark_price=models.DecimalField(max_digits=8,decimal_places=2) #100
    discount_percent=models.DecimalField(max_digits=4,decimal_places=2) #10 #99.99
    price=models.DecimalField(max_digits=8,decimal_places=2,editable=False) #90
    created_date=models.DateTimeField(auto_now=True)
    
    # price=100*(1-10/100) -->100*(1-0.1) -->100*(0.9) -->90
    
    def save(self,*args, **kwargs):
        self.price=self.mark_price*(1-self.discount_percent/100)
        super().save(*args, **kwargs)

class Order(models.Model):
    product=models.CharField(max_length=100)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    price=models.CharField(max_length=100)
    quantity=models.PositiveSmallIntegerField()
    total=models.CharField(max_length=100)
    image=models.ImageField(upload_to='order_image')
    is_pay=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=100)
    message=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

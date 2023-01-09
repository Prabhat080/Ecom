from distutils.command.upload import upload
from email.headerregistry import Address
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from numpy import product

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=30)
    phone = models.IntegerField(max_length=10)

    def __str__(self) -> str:
        return self.user.first_name+'_'+self.user.last_name+str(self.user.id)

class Product(models.Model):
    name = models.CharField(max_length=100)
    available = models.IntegerField()
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pics')
    def __str__(self) -> str:
        return self.name+str(self.id)

class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self) -> str:
        return self.customer.user.first_name+'_'+self.product.name+str(self.id)

class OrderHistory(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    delivery = models.CharField(default="P",max_length=20)
    date = models.DateField()
    payment = models.CharField(max_length=100)
    def __str__(self) -> str:
        return str(self.date)

class CheckoutCart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self) -> str:
        return self.customer.user.first_name+'_'+self.product.name+str(self.id)

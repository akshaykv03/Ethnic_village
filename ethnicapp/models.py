from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    phone=models.BigIntegerField()
    address=models.CharField(max_length=40)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class Manager(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    phone=models.BigIntegerField()
    address=models.CharField(max_length=40)
    district=models.CharField(max_length=40)
    village=models.CharField(max_length=40)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class Stay(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    phone=models.BigIntegerField()
    address=models.CharField(max_length=40)
    district=models.CharField(max_length=40)
    village=models.CharField(max_length=40)
    status=models.CharField(max_length=40,default="Available")
    image=models.ImageField()
    rate=models.IntegerField(null=True)
    user=models.ForeignKey(Manager,on_delete=models.CASCADE)
    

class Booking(models.Model):
    date=models.DateField(auto_now_add=True,null=True)
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    stay=models.ForeignKey(Stay,on_delete=models.CASCADE)
    from_date=models.DateField()
    to_date=models.DateField()
    total=models.IntegerField()
    status=models.CharField(max_length=30,null=True)


class Feedback(models.Model):
    date=models.DateField(auto_now_add=True)
    book=models.ForeignKey(Booking,on_delete=models.CASCADE)
    review=models.CharField(max_length=200)

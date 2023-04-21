from django.db import models
from LykaApp.models import Device
from LykaAccounts.models import Customer
from django.utils.timezone import now
from django.urls import reverse
import uuid

# Create your models here.

class Address(models.Model):
    billingName = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=10, blank = True, null = True)
    owner_of_address = models.ForeignKey(Customer, null = True, blank = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.billingName

    def getUid(self):
        return reverse('orderdetails', args=[self.orderid])

class Order(models.Model):
    customer = models.ForeignKey(Customer, blank = True, null = True, on_delete = models.CASCADE)
    orderid = models.CharField(max_length = 255)
    placeddate =  models.DateField(default = now)
    deliveryaddress = models.ForeignKey(Address, on_delete = models.CASCADE)
    deliverydate = models.DateField(default = now, blank = True, null = True)
    totalprice = models.IntegerField(default = 0)
    totalitems = models.IntegerField(default = 0)
    status = models.CharField(default = "Placed", max_length = 255)
    payment_method = models.CharField(blank = True, null = True, max_length = 255)
    tracking_id = models.CharField(default = uuid.uuid4, max_length = 255)
    payment_status = models.CharField(max_length = 255, null = True, blank = True)
    

    def __str__(self):
        return self.orderid
    

    

class OrderedItems(models.Model):
    orderlist = models.ForeignKey(Order, on_delete = models.CASCADE)
    product = models.ForeignKey(Device, on_delete = models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.brand + " " + self.product.modelName 
    
    def totalItemPrice(self):
        return self.product.price * self.quantity


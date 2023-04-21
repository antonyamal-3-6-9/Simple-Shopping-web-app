from django.db import models
from LykaApp.models import *
from datetime import date
from LykaAccounts.models import *

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length = 250)
    date_added = models.DateField(default=date.today())
    customer = models.ForeignKey(Customer, blank = True, null = True, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.cart_id
    

class CartItems(models.Model):
    cartlist = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Device, on_delete = models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.modelName
    
    def totalPriceItem(self):
        return self.product.price * self.quantity
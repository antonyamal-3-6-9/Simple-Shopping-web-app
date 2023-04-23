from django.contrib.auth.models import User
from django.db import models
import uuid
from django.utils.timezone import now



# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phno = models.IntegerField()
    uid = models.UUIDField(default = uuid.uuid4)
    
    def __str__(self):
        return self.user.username
    
class CardPaymentDetails(models.Model):
    nameOnCard = models.CharField(max_length = 50)
    cardNumber = models.CharField(max_length = 50)
    expiryDate = models.DateField(blank = True, null = True)
    cardType = models.CharField(max_length = 50)
    cardOwner = models.ForeignKey(Customer, on_delete = models.CASCADE, blank = True, null = True)
    
class UpiPaymentDetails(models.Model):
    upiId = models.CharField(max_length = 50)
    upiOwner = models.ForeignKey(Customer, on_delete = models.CASCADE, blank = True, null = True)
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import CustomerForm
from django.utils.timezone import now
import re
from datetime import date, datetime
from LykaOrders.models import *

def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def is_valid_mobile_number(number):
    pattern = r'^\+?[0-9]{10}$'
    return bool(re.match(pattern, number))


def register(request):
    form = CustomerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username=form.cleaned_data['username']
        password1=form.cleaned_data['password1']
        password2=form.cleaned_data['password2']
        phno=form.cleaned_data['phno']
        dob=form.cleaned_data['dob']

        
        # date_obj = datetime.strptime(dob, '%Y-%m-%d').date()
        if not is_valid_mobile_number(phno):
            messages.warning(request, "mobile number is Invalid")
            return redirect('register')
        if calculate_age(dob) < 5:
            messages.warning(request, "You have to be atleast 5 years old") 
            return redirect('register')
        if password1 != password2:
            messages.warning(request, "passwords are not matching")
            return redirect('register')




        if User.objects.filter(username = username).exists():
            messages.info(request, "User Already Exists, Try a different username")
            return redirect("register")
        else:
            customer = form.save()
        user = authenticate(username = username, password = password1)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request, 'register.html', {'form' : form})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        passw = request.POST['password']
        if User.objects.filter(username = username).exists():
            user = authenticate(username = username, password = passw)
        else:
            messages.info(request, "User not found")
            return redirect('login')
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('home')


def profile(request):
    items = None
    custom = Customer.objects.get(user = request.user)
    order = Order.objects.filter(customer = custom)
    address = Address.objects.filter(owner_of_address = custom)
    creditcards = CardPaymentDetails.objects.filter(cardOwner = custom, cardType = "Credit Card")
    debitcards = CardPaymentDetails.objects.filter(cardOwner = custom, cardType = "Debit Card")
    upis = UpiPaymentDetails.objects.filter(upiOwner = custom)
    for i in order:
        items = OrderedItems.objects.filter(orderlist = i)
    
    context = {"customer" : custom, "orders" : order, "address" : address, "creditcards" : creditcards, "debitcards" : debitcards, "upis" : upis, "items" : items}
    return render(request, "profile.html", context)
    
    

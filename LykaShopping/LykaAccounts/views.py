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

def validate_name(name):
    pattern = "^[A-Za-z]+(?:\s[A-Za-z]+)+$"
    if re.match(pattern, name):
        return True
    else:
        return False

def register(request):
    form = CustomerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username=form.cleaned_data['username']
        password1=form.cleaned_data['password1']
        password2=form.cleaned_data['password2']
        phno=form.cleaned_data['phno']

        

        if not is_valid_mobile_number(phno):
            messages.warning(request, "mobile number is Invalid")
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
    items = []
    custom = Customer.objects.get(user = request.user)
    order = Order.objects.filter(customer = custom)
    address = Address.objects.filter(owner_of_address = custom)
    creditcards = CardPaymentDetails.objects.filter(cardOwner = custom, cardType = "Credit Card")
    debitcards = CardPaymentDetails.objects.filter(cardOwner = custom, cardType = "Debit Card")
    upis = UpiPaymentDetails.objects.filter(upiOwner = custom)
    for i in order:
        item = OrderedItems.objects.filter(orderlist = i)
        items.extend(item)
    
    context = {"customer" : custom, "orders" : order, "address" : address, "creditcards" : creditcards, "debitcards" : debitcards, "upis" : upis, "items" : items}
    return render(request, "profile.html", context)




def editAddress(request, addId):
    address = Address.objects.get(id = addId)
    editAddressUrl = reverse('editaddress', kwargs = {"addId" : addId})
    if request.method == "POST":
        name = request.POST.get('billingName')
        phone = request.POST.get('phone')
        add1 = request.POST.get('address1')
        add2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zipCode = request.POST.get('zip')

        if not validate_name(name) or not bool(name):
            messages.warning(request, "Invaid Name")
            return redirect(editAddressUrl)
        if not is_valid_mobile_number(phone) or not bool(phone):
            messages.warning(request, "Invalid Phone Number")
            return redirect(editAddressUrl)
        if not len(add1) < 5:
            messages.warning(request, "Invalid Address")
            return redirect(editAddressUrl)
        if not len(add2) <5:
            messages.warning(request, "Invalid Address")
            return redirect(editAddressUrl)
        if not len(zipCode) == 6:
            messages.warning(request,"Invalid zipcode")
            return redirect(editAddressUrl)
        if not bool(city) or not bool(state) or not bool(country) or not bool(name) or not bool(phone) or not bool(add1) or not bool(add2) or bool(zipCode):
            messages.warning(request, "Fields Must Not be Empty")
            return redirect(editAddress)
    


        if address.billingName != name:
            address.billingName = name
            address.save()
        if address.phone_number != phone:
            address.phone_number = phone
            address.save()
        if address.address_line_1 != add1:
            address.address_line_1 = add1
            address.save()
        if address.address_line_2 != add2:
            address.address_line_2 = add2
            address.save()
        if address.city != city:
            address.city = city
            address.save()
        if address.state != city:
            address.state = state
            address.save()
        if address.country != country:
            address.country = country
            address.save()
        if address.zip_code != zipCode:
            address.zip_code = zipCode
            address.save()
        return redirect('profile')
    else:
        return render(request, "addressedit.html", {"address" : address})
    


def deleteAddress(request, addId):
    address = Address.objects.get(id = addId)
    address.owner_of_address = None;
    messages.success(request, "Successfully Deleted")
    return redirect('profile')
    
def addNewAddress(request):
    if request.method == "POST":
        name = request.POST.get('billingName')
        phone = request.POST.get('phone')
        add1 = request.POST.get('address1')
        add2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zipCode = request.POST.get('zip')

        owner = Customer.objects.get(user = request.user)

        if not is_valid_mobile_number(phone):
            messages.warning(request, "Invalid Phone Number")
            return redirect('addnewaddress')
        if len(add1) < 5:
            messages.warning(request, "Invalid Address")
            return redirect('addnewaddress')
        if len(add2) < 5:
            messages.warning(request, "Invalid Address")
            return redirect('addnewaddress')
        if not len(zipCode) == 6:
            messages.warning(request,"Invalid zipcode")
            return redirect('addnewaddress')
        if not bool(city) or not bool(state) or not bool(country) or not bool(name) or not bool(phone) or not bool(add1) or not bool(add2) or not bool(zipCode):
            messages.warning(request, "Fields Must Not be Empty")
            return redirect('addnewaddress')
    
        address = Address.objects.create(
            billingName=name,
            address_line_1=add1,
            address_line_2=add2,
            city=city,
            state=state,
            country=country,
            zip_code=zipCode,
            phone_number=phone,
            owner_of_address=owner
        )
        messages.success(request, "New address has been added")
        return redirect('profile')
    else:
        return render(request, 'addressadd.html')
    

def updateCustomer(request, customerId):
    updateUrl = reverse('update', kwargs = {"customerId" : customerId})
    custom = Customer.objects.get(uid = customerId)
    if request.method == "POST":
        if "user-submit-button" in request.POST:
            firstName = request.POST.get('first-name')
            lastName = request.POST.get('last-name')
            phNo = request.POST.get('phone-number')
            userName = request.POST.get('username')
            emailId = request.POST.get('email-id')


            if not bool(firstName) or not bool(lastName) or not bool(emailId) or not bool(userName) or not bool(phNo):
                messages.warning(request, "Fields Must not be Empty")
                return redirect(updateUrl)


            if not is_valid_mobile_number(phNo):
                messages.warning(request, "Invaid Phone Number")
                return redirect(updateUrl)
        

            if custom.user.first_name != firstName:
                custom.user.first_name = firstName
                custom.user.save()
                custom.save()
            if custom.user.last_name != lastName:
                custom.user.last_name = lastName
                custom.user.save()
                custom.save()
            if custom.user.email != emailId:
                custom.user.email = emailId
                custom.user.save()
                custom.save()
            if custom.user.username != userName:
                if User.objects.filter(username = userName).exists():
                    messages.warning(request, "Username is taken")
                    return redirect(updateUrl)
                custom.user.username = userName
                custom.user.save()
                custom.save()
            if custom.phno == phNo:
                custom.phno = phNo
                custom.save()
            messages.success(request, "User Profile Updated successfully")
            return redirect('profile')
        elif "password-submit-button" in request.POST:
            existingPassword = request.POST.get('old_password')
            newPassword1 = request.POST.get('new_password1')
            newPassword2 = request.POST.get('new_password2')

            if not bool(newPassword1) or not bool(newPassword2):
                messages.warning(request, "Password cannot be an empty string")
                return redirect(updateUrl)

            if custom.user.check_password(existingPassword):
                if newPassword1 == newPassword2:
                        custom.user.set_password(newPassword1)
                        custom.user.save()
                        custom.save()
                        user = authenticate(username = custom.user.username, password = newPassword1)
                        auth.login(request, user)
                        
                else:
                    messages.warning(request, "Passwords are not matching")
                    return redirect(updateUrl)
            else:
                messages.warning(request, "Existing password is incorrect, Try again")
                return redirect(updateUrl)
            messages.success(request, "Password Updated Successfully")
            return redirect('profile')
    else:
        return render(request, 'updateuser.html', {"customer" : custom})
    


def deletePayment(request, paymentMethod, paymentId):
    if paymentMethod == "Credit Card" or paymentMethod == "Debit Card":
        card = CardPaymentDetails.objects.get(id = paymentId)
        card.delete()
        messages.success(request, "Card has been deleted successfully")
        return redirect('profile')
    if paymentMethod == "UPI":
        upi = UpiPaymentDetails.objects.get(id = paymentId)
        upi.delete()
        messages.success(request, "Upi has been deleted successfully")
        return redirect('profile')



    
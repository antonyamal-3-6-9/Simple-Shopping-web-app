from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from LykaCart.models import *
from LykaAccounts.models import *
from . forms import AddressForm
from . models import *
import uuid
import datetime
from django.contrib import messages
import re
# Create your views here.

today = datetime.date.today()
shippingDay = today + datetime.timedelta(days=3)
delivery = today + datetime.timedelta(days=7)



def validate_name(name):
    pattern = "^[A-Za-z]+(?:\s[A-Za-z]+)+$"
    if re.match(pattern, name):
        return True
    else:
        return False
    


def is_valid_mobile_number(number):
    pattern = r'^\+?[0-9]{10}$'
    return bool(re.match(pattern, number))


def checkout(request):
    totalPrice = 0
    itemCount = 0
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        custom = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(cart_id=custom.uid, customer = custom)
        cartItems = CartItems.objects.filter(cartlist=cart)
        address = Address.objects.filter(owner_of_address=custom)
        for item in cartItems:
            totalPrice += item.product.price * item.quantity
            itemCount += item.quantity
    return render(request, "checkout.html", {"total": totalPrice, "count": itemCount, "cartitem": cartItems, "address": address})


def verify(request):
    orderid = None
    custom = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(cart_id=custom.uid, customer = custom)
    cartItems = CartItems.objects.filter(cartlist=cart)


    if request.method == "POST":
        if "ExistingSubmit" in request.POST:
            addressId = request.POST.get('address')
            address = Address.objects.get(id=addressId, owner_of_address=custom)
        elif "newSubmit" in request.POST:
            billName = request.POST.get('firstName') + " " + request.POST.get('lastName')
            phno = request.POST.get('phone')
            add1 = request.POST.get('address1')
            add2 = request.POST.get('address2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zip')
            country = request.POST.get('country')
            owner = request.POST.get('address-owner')
            print("new submit")

            if not bool(city) or not bool(state) or not bool(country) or not bool(add1) or not bool(add2) or not bool(zipcode) or not bool(billName) or not bool(phno):
                messages.warning(request, "Fields Must not be Empty")
                return redirect('checkout')

            if not is_valid_mobile_number(phno):
                messages.warning(request, "Invalid Phone Number")
                return redirect("checkout")
            if len(add1) < 5:
                messages.warning(request, "Invalid Address")
                return redirect("checkout")
            if len(add2) < 5:
                messages.warning(request, "Invalid Address")
                return redirect("checkout")
            if not len(zipcode) == 6:
                messages.warning(request,"Invalid zipcode")
                return redirect('checkout')

            


            address = Address.objects.create(
                billingName=billName,
                address_line_1=add1,
                address_line_2=add2,
                city=city,
                state=state,
                country=country,
                zip_code=zipcode,
                phone_number=phno
            )
            if owner == "checked":
                address.owner_of_address = custom
                address.save()

        order = Order.objects.create(
            customer=custom,
            orderid=uuid.uuid1(),
            deliveryaddress=address,
            deliverydate=delivery
        )
        for i in cartItems:
            orderedItems = OrderedItems.objects.create(
                orderlist=order, product=i.product, quantity=i.quantity)
            order.totalprice += orderedItems.product.price * orderedItems.quantity
            order.totalitems += orderedItems.quantity
            order.save()
        ordereditems = OrderedItems.objects.filter(orderlist = order)
        return render(request, 'itemandaddress.html', {'order' : order, 'ordereditems' : ordereditems})
    else:
        return redirect('checkout')


def myorder(request):
    orderedItems = []
    custom = Customer.objects.get(user=request.user)
    order = Order.objects.filter(customer=custom)
    for i in order:
        items = OrderedItems.objects.filter(orderlist = i)
        orderedItems.extend(items)
        if i.deliverydate < today or i.deliverydate == today:
            i.status = "Delivered"
            i.save()
        elif i.deliverydate < shippingDay or i.deliverydate == shippingDay:
            i.status = "Shipped"
            i.save()
    return render(request, 'myorders.html', {'orders': order, 'items' : orderedItems})


def cardMasking(cardNumber):
    numLen = len(cardNumber)
    if numLen == 15:
        masked_card_number = '{} ***** **** {}'.format(
            cardNumber[:3],
            cardNumber[-3:]
        )
    elif numLen == 16:
        masked_card_number = '{} **** **** {}'.format(
            cardNumber[:4],
            cardNumber[-4:]
        )
    elif numLen == 17:
        masked_card_number = '{} **** ***** {}'.format(
            cardNumber[:4],
            cardNumber[-4:]
        )
    elif numLen == 18:
        masked_card_number = '{} ***** ***** {}'.format(
            cardNumber[:4],
            cardNumber[-4:]
        )
    elif numLen == 19:
        masked_card_number = '{} ****** ***** {}'.format(
            cardNumber[:4],
            cardNumber[-4:]
        )
    return masked_card_number


def is_valid_upi(upi_id):
    pattern = r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+$'
    return bool(re.match(pattern, upi_id))


def payment(request, orderId):
    custom = Customer.objects.get(user=request.user)
    creditCardDetails = CardPaymentDetails.objects.filter(cardOwner=custom, cardType="Credit Card")
    debitCardDetails = CardPaymentDetails.objects.filter(cardOwner=custom, cardType="Debit Card")
    upiDetails = UpiPaymentDetails.objects.filter(upiOwner=custom)
    return render(request, 'payment.html', {'creditcards' : creditCardDetails, 'debitcards' : debitCardDetails, 'upis' : upiDetails, 'orderId' : orderId} )



def removeCart(custom):
    cart = Cart.objects.get(cart_id = custom.uid, customer = custom)
    cartItems = CartItems.objects.filter(cartlist = cart)
    for i in cartItems:
        i.delete()
    



def ordercompleted(request, orderId):
    custom = Customer.objects.get(user=request.user)
    order = Order.objects.get(orderid=orderId)
    payment_url = reverse('payment', kwargs = {'orderId' : orderId})
    if request.method == 'POST':
        paymentMethod = request.POST.get('paymentMethod')
        if paymentMethod == "credit-card":
            savedCreditCard = request.POST.get('creditcard')
            addNewCreditCardRadio = request.POST.get('add-credit-card-radio')
            cvv = request.POST.get("cvvsavedcredit")
            if bool(savedCreditCard) and bool(cvv) and len(cvv) == 3:
                card = CardPaymentDetails.objects.get(id=savedCreditCard, cardOwner=custom, cardType="Credit Card")
                if card is not None:
                    order.payment_method = paymentMethod
                    order.payment_status = "Paid"
                    order.save()
                    removeCart(custom)
                    return render(request, "itemordered.html")
                else:
                    messages.warning(request, "Credit Card details not given")
                    return redirect(payment_url)
            elif addNewCreditCardRadio == "add-credit-card":
                owner = request.POST.get("cc-owner")
                name = request.POST.get("credit-card-name")
                number = request.POST.get("credit-card-number")
                date = request.POST.get("credit-card-expiry")
                cvvNum = request.POST.get("credit-card-cvv")

                date_obj = None
                if bool(date):
                    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                else:
                    messages.warning(request, "Invalid Date")
                    return redirect(payment_url)

                if not validate_name(name = name):
                    messages.warning(request, "Invalid Name")
                    return redirect(payment_url)
                if not len(number) >= 15 and not len(number) <= 19:
                    messages.warning(request, "Invalid Card NUmber")
                    return redirect(payment_url)
                if not date_obj > today:
                    messages.warning(request, "Invalid Date")
                    return redirect(payment_url)
                if not len(cvvNum) == 3:
                    messages.warning(request, "Invalid CVV")
                    return redirect(payment_url)                    
                cardNumber = cardMasking(str(number))
                card = CardPaymentDetails.objects.create(
                    nameOnCard=name,
                    cardNumber=cardNumber,
                    expiryDate=date_obj,
                    cardType="Credit Card",
                )
                if card is not None:
                    order.payment_method = paymentMethod
                    order.payment_status = "Paid"
                    order.save()
                    removeCart(custom)
                    if owner == "checked":
                        card.cardOwner = custom
                        card.save()
                    else:
                        card.delete()
                    return render(request, "itemordered.html")
                else:
                    messages.warning(request, "Credit Card details not given")
                    return redirect(payment_url)


            else:
                messages.warning(request, "Invalid CVV, Try again")
                return redirect(payment_url)
    
        elif paymentMethod == "debit-card":
            savedDebitCard = request.POST.get('debitcard')
            addNewDebitCardRadio = request.POST.get('add-debit-card-radio')
            cvv = request.POST.get("cvvsaveddebit")
            if bool(savedDebitCard) and bool(cvv) and len(cvv) == 3:
                card = CardPaymentDetails.objects.get(id=savedDebitCard, cardOwner=custom, cardType="Debit Card")
                if card is not None:
                    order.payment_method = paymentMethod
                    order.payment_status = "Paid"
                    order.save()
                    removeCart(custom)
                    return render(request, "itemordered.html")
                else:
                    messages.warning(request, "Debit Card details not given")
                    return redirect(payment_url)
            elif addNewDebitCardRadio == "add-debit-card":
                owner = request.POST.get("dc-owner")
                name = request.POST.get("debit-card-name")
                number = request.POST.get("debit-card-number")
                date = request.POST.get("debit-card-expiry")
                cvvNum = request.POST.get("debit-card-cvv")
                
                date_obj = None
                if bool(date):
                    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                else:
                    messages.warning(request, "Invalid Date")
                    return redirect(payment_url)

                if not validate_name(name = name):
                    messages.warning(request, "Invalid Name")
                    return redirect(payment_url)
                if not len(number) >= 15 and len(number) <= 19:
                    messages.warning(request, "Invalid Card NUmber")
                    return redirect(payment_url)
                if not date_obj > today:
                    messages.warning(request, "Invalid Date")
                    return redirect(payment_url)
                if not len(cvvNum) == 3:
                    messages.warning(request, "Invalid CVV")
                    return redirect(payment_url)                  


                cardNumber = cardMasking(str(number))
                card = CardPaymentDetails.objects.create(
                    nameOnCard=name,
                    cardNumber=cardNumber,
                    expiryDate=date_obj,
                    cardType="Debit Card",
                    )
      

                if card is not None:
                    order.payment_method = paymentMethod
                    order.payment_status = "Paid"
                    order.save()
                    removeCart(custom)
                    if owner == "checked":
                        card.cardOwner = custom
                        card.save()
                    else:
                        card.delete()
                    return render(request, "itemordered.html")
                else:
                    messages.warning(request, "Debit Card details not given")
                    return redirect(payment_url)


            else:
                messages.warning(request, "Invalid CVV, Try again")
                return redirect(payment_url)

        elif paymentMethod == "upi-id-payment":
            savedUpi = request.POST.get("upi-id")
            addNewUpi = request.POST.get("add-new-upi-id-radio")
            if bool(savedUpi):
                upi = UpiPaymentDetails.objects.get(id=savedUpi, upiOwner=custom)
                if upi is not None:
                    order.payment_method = paymentMethod
                    order.payment_status = "Paid"
                    order.save()
                    removeCart(custom)
                    return render(request, "itemordered.html")
                else:
                    return redirect(payment_url)
            elif addNewUpi == "add-new-upi-id":
                upiid = request.POST.get('new-upi-id')
                owner = request.POST.get('upi-owner')
                if is_valid_upi(upiid):
                    upi = UpiPaymentDetails.objects.create(upiId=upiid)
                else:
                    messages.warning(request, "Invalid UPI Id")
                    return redirect(payment_url)

                if upi is not None:
                    order.payment_method = paymentMethod
                    order.payment_status = "Paid"
                    order.save()
                    removeCart(custom)
                    if owner == "checked":
                        upi.upiOwner = custom
                        upi.save()
                    else:
                        upi.delete()
                    return render(request, "itemordered.html")
                else:
                    messages.warning(request, "Upi details are not given")
                    return redirect(payment_url)


            else:
                messages.warning(request, "Invalid Upi Try Again")
                return redirect(payment_url)
            
        elif paymentMethod == "cod-payment":
            order.payment_method = "Cash On Delivery"
            order.payment_status = "Pending"
            order.save()
            removeCart(custom)
            return render(request, "itemordered.html")
        else:
            messages.warning(request, "Try Again")
            return redirect(payment_url)
    else:
        return redirect(payment_url)


def orderdetails(request, orderId):
    order = Order.objects.get(orderid= orderId)
    details = OrderedItems.objects.filter(orderlist = order)
    return render(request, 'orderdetails.html', {'details': details, 'orderlist' : order})


def cancelorder(request, orderId):
    order = Order.objects.get(orderid= orderId)
    orderedItems = OrderedItems.objects.filter(orderlist= order)
    for i in orderedItems:
        i.product.stock += i.quantity
        i.product.save()
        i.save()
    order.status = "Cancelled"
    order.save()
    return redirect('myorder')


def denied(request, orderId):
    order = Order.objects.get(orderid = orderId)
    orderedItems = OrderedItems.objects.filter(orderlist= order)
    for i in orderedItems:
        i.delete()
    order.delete()
    return redirect('home')

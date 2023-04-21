from django.shortcuts import redirect, render
from .models import *
from LykaApp.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib.sessions.backends.db import SessionStore

# Create your views here.



def displayCart(request, totalPrice = 0, itemCount = 0, cartItems = None):
    if not request.user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id = cartId(request))
        except ObjectDoesNotExist:
            return render(request, 'cart.html')
    else:
        custom = Customer.objects.get(user = request.user)
        try:
            cart = Cart.objects.get(cart_id = custom.uid)
        except ObjectDoesNotExist:
            return render(request, 'cart.html')
    cartItems = CartItems.objects.filter(cartlist = cart)
    for item in cartItems:
        totalPrice += item.product.price * item.quantity
        itemCount += item.quantity
    return render(request, "cart.html", {"total" : totalPrice, "count" : itemCount, "cartitem" :cartItems })

def cartId(request):
    cid = request.session.session_key
    if not SessionStore().exists(request.session.session_key):
        cid = request.session.create()
    return cid

def addToCart(request, productId):
    product = Device.objects.get(id = productId)
    if not request.user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id = cartId(request))
        except ObjectDoesNotExist:
            cart = Cart.objects.create(cart_id = cartId(request))
            cart.save()
    else:
        custom = Customer.objects.get(user = request.user)
        try:
            cart = Cart.objects.get(cart_id = custom.uid)
        except ObjectDoesNotExist:
            cart = Cart.objects.create(cart_id = custom.uid)
            cart.save()
    try:
        cartItems = CartItems.objects.get(cartlist = cart, product = product)
        if product.stock > 0:
            cartItems.quantity += 1
        cartItems.save()
    except ObjectDoesNotExist:
        cartItems = CartItems.objects.create(cartlist = cart, product = product, quantity = 0)
        if product.stock > 0:
            cartItems.quantity += 1
        cartItems.save()
    route = product.getUrlDev()
    print(route)
    return redirect(route)


def incrementItem(request, product_id):
    if not request.user.is_authenticated:
        cart = Cart.objects.get(cart_id = cartId(request))
    else:
        custom = Customer.objects.get(user = request.user)
        cart = Cart.objects.get(cart_id = custom.uid)
    product = Device.objects.get(id=product_id)
    cartItem = CartItems.objects.get(product = product, cartlist = cart)
    if product.stock > 0:
        cartItem.quantity += 1
        product.stock -= 1
        cartItem.save()
        product.save()
    return redirect ("displaycart")


def decrementItem(request, product_id):
    if not request.user.is_authenticated:
        cart = Cart.objects.get(cart_id = cartId(request))
    else:
        custom = Customer.objects.get(user = request.user)
        cart = Cart.objects.get(cart_id = custom.uid)
    product = Device.objects.get(id = product_id)
    cartItem = CartItems.objects.get(product = product, cartlist = cart)
    if cartItem.quantity > 1:
        cartItem.quantity -= 1
        product.stock += 1
        cartItem.save()
        product.save()
    elif cartItem.quantity == 1:
        cartItem.delete()
    return redirect ("displaycart")


def deleteItem(request, product_id):    
    if not request.user.is_authenticated:
        cart = Cart.objects.get(cart_id = cartId(request))
    else:
        custom = Customer.objects.get(user = request.user)
        cart = Cart.objects.get(cart_id = custom.uid)
    product = Device.objects.get(id = product_id)
    cartItem = CartItems.objects.get(product = product, cartlist = cart)
    cartItem.delete()
    return redirect ("displaycart")
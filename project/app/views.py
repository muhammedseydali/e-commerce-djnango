from ast import Or
from ctypes import addressof
from functools import total_ordering
from math import prod
from sqlite3 import complete_statement
from statistics import quantiles
from venv import create
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart,cartData,guestOrder

# Create your views here.
def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
   
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'CartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):

    data = cartData(request)
    CartItems = data['cartItems']
    order = data['order']
    items = data['items']
            
    context = {'items':items, 'order':order, 'cartItems':CartItems}
    return render(request, 'store/cart.html', context)


def UpdateItem(request):
    data  = json.loads(request.data)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:',productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Product.objects.get_or_create(customer=customer, complete=False)

    OrderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        OrderItem.quantity = (OrderItem.quantity +1)
    elif action == 'remove':
            OrderItem.quantity = (OrderItem.quantity -1)
    OrderItem.save()

    if OrderItem.quantity <= 0:
        OrderItem.delete()        

    return JsonResponse('item was added', safe=False)    

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ProcessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)


    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
           

        
    else:
        customer,order = guestOrder(request, data)

    total = float(data['form']['total'])
    order_transaction_id = transaction_id 

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()   

    if order.shipping  == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )      
    print('Data:', request)
    return JsonResponse('payment complete', safe=False)    
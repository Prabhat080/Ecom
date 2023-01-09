import email
import imp
import json
from django import views
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,Group
from django.contrib.auth import logout
from django.contrib import auth
from requests import Response
from .models import *
import random
import datetime
def adminView(request):
    user = request.user
    group = request.user.groups
    if group.filter(name='admin').exists():
        checkoutCart =  list(CheckoutCart.objects.all())
        return render(request,'ecommerce/checkoutCart.html',context={'checkoutCart':checkoutCart})
    else:
        return HttpResponse("Not Authorised")
def home(request):
    return render(request,'ecommerce/home.html')

def registerAdmin(request):
    if request.method == 'GET':
        return render(request,'ecommerce/register.html') 
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        username = email.split('@')[0]
        group = Group.objects.get(name='admin')
        if User.objects.filter(username=username).exists(): 
            return redirect('Login')
        else:
            user = User.objects.create_user(username = email.split('@')[0],email=email,password=password)
            user.first_name=first_name
            user.last_name=last_name
            user.set_password(password)
            user.save()
            user.groups.add(group)
            user.save()
            customer = Customer(user=user,phone=phone,address=address)
            customer.save()
            return render(request,'ecommerce/home.html',context={'f':first_name})
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        username = email.split('@')[0]
        group = Group.objects.get(name='customer')
        if User.objects.filter(username=username).exists(): 
            return redirect('Login')
        else:
            user = User.objects.create_user(username = email.split('@')[0],email=email,password=password)
            user.first_name=first_name
            user.last_name=last_name
            user.set_password(password)
            user.save()
            user.groups.add(group)
            user.save()
            customer = Customer(user=user,phone=phone,address=address)
            customer.save()
            return render(request,'ecommerce/home.html',context={'f':first_name})
    else:
        return render(request,'ecommerce/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user=user)
            return render(request,'ecommerce/home.html',context={'f':"Hello There!"})
        else:
            return redirect('Register')
    else:
        return render(request,'ecommerce/login.html')

def logout(request):
    auth.logout(request)
    return redirect("Home")

def ListProduct(request):
    print(Product.objects.all())
    return render(request,'ecommerce/ProductsList.html',context={'productDictionary':Product.objects.all()})
# Create your views here.

def product(request,pk):
    product = Product.objects.get(pk=int(pk))
    return render(request,'ecommerce/Product.html',context={'Product':product})

def categoryView(request,category):
    categoryList = Product.objects.filter(category=category)
    return render(request,'ecommerce/Category.html',{'categoryList':categoryList,'category':category})

def updItem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        product = Product.objects.get(id=int(productId))
        customer = Customer.objects.get(user=request.user)
        available = product.available
        if action == 'add':
            if Cart.objects.filter(customer=customer,product=product).exists():
                cart = Cart.objects.get(customer=customer,product=product)
                if cart.quantity+1<=available:
                    cart.quantity = cart.quantity+1
                    cart.save()
            else:
                if available>0:
                    cart = Cart(customer=customer,product=product,quantity=1)
                    cart.save()
        return JsonResponse({"A":"B"})

def cart(request):
    if request.method == "POST":
        return HttpResponse("Hello")
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        carts = Cart.objects.filter(customer=customer)
        return render(request,'ecommerce/cart.html',context={'carts':carts})
    return redirect('Login')

def updQuantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        product = Product.objects.get(id=int(productId))
        customer = Customer.objects.get(user=request.user)
        max_quantity = product.available
        if action == 'add':
            cart = Cart.objects.get(customer=customer,product=product)
            if cart.quantity < max_quantity:
                cart.quantity = cart.quantity+1
            cart.save()
        elif action == 'del':
            cart = Cart.objects.get(customer=customer,product=product)
            if cart.quantity == 1:
                cart.quantity = 0
                cart.delete()
            else:
                cart.quantity = cart.quantity-1
                cart.save()  
        return JsonResponse({'quantity':cart.quantity})   
    return JsonResponse({"A":"B"})
  
def checkout(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        cart = list(Cart.objects.filter(customer=customer))
        if len(cart)==0:
            return redirect('normal')
        else:
            return render(request,'ecommerce/checkout.html')
    else:
        redirect('Login')
    return HttpResponse("Hello World")

def online(request):
    return render(request,'ecommerce/payment_page.html')

def fake_payment(request):
    d = (random.randint(0,100))%2
    if d==0:
        ch = "NO"
    else:
        ch = "OK"
    return JsonResponse({"status":ch})

def inventory(request):
    user = request.user

    grps = user.groups

    if grps.filter(name="admin").exists():
        return redirect('Home')
    else:
        return HttpResponse(status=404)

def updateCart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except:
            data = "null"
        if data!="null" and data['status'] == "OK":
            user = request.user
            customer = Customer.objects.get(user=user)
            carts = list(Cart.objects.filter(customer=customer))
            for cart in carts:
                product = cart.product
                quantity = cart.quantity
                checkoutCart = CheckoutCart(customer=customer,product=product,quantity=quantity)
                checkoutCart.save()
                orderHistory = OrderHistory(customer=customer,product=product,quantity=quantity,payment="Online",date = datetime.datetime.now().date())
                product.available = product.available - quantity
                product.save()
                orderHistory.save()
                cart.delete()
            return JsonResponse({"connection":"ok"})
        else:
            return JsonResponse({"notOK":"a"})
    else:
        return JsonResponse({"notOK2":"a"})

def orderHistory(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    orders = list(OrderHistory.objects.filter(customer=customer))
    return render(request,'ecommerce/orderHistory.html',context={"orders":orders})

def updOrderHistory(request):
    if request.method == "POST":
        data = json.loads(request.body)
        productId = data['productId']
        customerId = data['customerId']
        cartId = data['cartId']
        delivery_status = data['status']
        customer = Customer(id=customerId)
        product = Product(id=productId)
        order_history = OrderHistory.objects.get(product=product,customer=customer)
        order_history.delivery = delivery_status
        order_history.save()
        cart = CheckoutCart(id=cartId)
        cart.delete()
        return JsonResponse({"status":"changed"})
    else:
        return JsonResponse({"Method":"Incorrect"})

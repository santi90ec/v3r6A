import re
from typing import cast
from django.db.models.query import RawQuerySet
from django.http import request
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import User,Profile, Address, Product, ProductCategory, Warehouse, Cart, CartProduct
from django.conf import settings
import bcrypt

from main import models

# Create your views here.
def loginIndex(request):
    return render(request,'logi.html')
def createUser (request):
    if request.method=='POST':
        errors=User.objects.userValidator(request.POST)
        if len(errors)>0:
            for key,value in errors.items():
                
                messages.error(request,value)
            return redirect('/')
        hash_pw=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        profileUser=Profile.objects.get(id=1)
        new_user=User.objects.create(
            firstName=request.POST['firstName'],
            lastName=request.POST['lastName'],
            email=request.POST['email'],
            password=hash_pw,
            profileId=profileUser
        )
        request.session['logged_user']=new_user.id
        return redirect('/home')
    return redirect('/')
def login(request):
    if request.method=='POST':
        errors=User.objects.loginValidator(request.POST)
        if len(errors)>0:
            for key,value in errors.items():
                
                messages.error(request,value)
            return redirect('/')
        user=User.objects.filter(email=request.POST['usrEmail'])
        if user:
            log_user=user[0]
            if bcrypt.checkpw(request.POST['usrPass'].encode(), log_user.password.encode()):
                request.session['logged_user']=log_user.id
                return redirect('/home')
            messages.error(request,"Email/Password incorrect")
    return redirect('/')
def homeIndex(request):
    user=User.objects.get(id=request.session['logged_user'])
    context = {'google_api_key': settings.GOOGLE_API_KEY,
                'user': user,
                'direcciones': Address.objects.filter(user__id=request.session['logged_user']),
                'products': Warehouse.objects.filter(quantity__gte=0),
        }
    if 'current_cart' in request.session:
        cart=Cart.objects.filter(id=request.session['current_cart'])
        context['car']=cart    
    if user.profileId.id == 1:
        return render(request,'index.html' , context)
    if user.profileId.id == 2:
        return redirect('/admin/index')
def logout(request):
    request.session.flush()
    return redirect('/')
def createAddress(request):
    if request.method=='POST':
        a =request.POST.get('id_lat', False)
        print(a)
        add=Address.objects.create(
            description=request.POST['txtCasa'],
            lat=request.POST.get('id_lat', False),
            lon=request.POST.get('id_lng', False),
            user=User.objects.get(id=request.session['logged_user'])
        )
        return redirect('/home')
def deleteAddress(request, idAdd):
    addr=Address.objects.get(id=idAdd)
    addr.delete()
    return redirect ('/home/profile')
def profile(request):
    user=User.objects.get(id=request.session['logged_user'])
    context = {'google_api_key': settings.GOOGLE_API_KEY,
                'user': user,
                'direcciones': Address.objects.filter(user__id=request.session['logged_user']),
                'products': Warehouse.objects.filter(quantity__gte=0)
        }
    if 'current_cart' in request.session:
        cart=Cart.objects.filter(id=request.session['current_cart'])
        context['car']=cart    
    return render(request,'profile.html',context)
def addProduct2Cart(request,idProd):
    if 'current_cart' not in request.session:
        new_cart=Cart.objects.create(
            user=User.objects.get(id=request.session['logged_user']),
            status="O"
        )
        request.session['current_cart']=new_cart.id
        price=Product.objects.get(id=idProd)
        new_prod=CartProduct.objects.create(
            cart=new_cart,
            product=Product.objects.get(id=idProd),
            quantity=+1,
            total_price=float(price.unitPrice)
        )
        new_cart.total+=new_prod.total_price
        new_cart.save()
        return redirect('/home')
    cart=Cart.objects.filter(id=request.session['current_cart'])
    prod=Product.objects.get(id=idProd)
    new_prod=CartProduct.objects.get_or_create(
        cart=cart,
        quantity=+1,
        product=prod,
        total_price=float(prod.unitPrice)
    )
    cart.total+=prod.unitPrice
    cart.save()

    return redirect('/home')
def cart(request):
    content={
        'address': Address.objects.filter(user=request.session['logged_user']),
        'car':Cart.objects.filter(id=request.session['current_cart'])
    }
    return render(request,'cart.html',content)
def deleteCart(request):
    car=Cart.objects.filter(id=request.session['current_cart'])
    if car.status == "O" or car.status == "C":
        car.status="X"
        del request.session['current_cart']
    else:
        del request.session['current_cart']
    return redirect('/home')
def orderCart(request):
    if request.method=='POST':    
        Cart.objects.filter(id=request.session['current_cart']).update(
            status="C",
            address=Address.objects.get(id=request.POST['dire'])
            
            )
        return redirect('/home')
##################################################
##      ADMIN VIEWS ######
##################################################
def adminIndex(request):
    context = { 
        'user': User.objects.get(id=request.session['logged_user']),
        'otherOrders': Cart.objects.all()
    }
    orders=Cart.objects.filter(status="C")
    if orders:    
        context['orders']=orders       
    return render (request,'admin/admin.html', context)

def editIndex(request):
    context ={
        'user': User.objects.get(id=request.session['logged_user']),
        'products': Warehouse.objects.all(),
        'categoria': ProductCategory.objects.all()        
    }
    orders=Cart.objects.filter(status="C")
    if orders:    
        context['orders']=orders 
    return render(request, 'admin/edit.html', context)
def createProduct(request):
    if request.method=='POST':
        product = Product.objects.create(
            description = request.POST['producto'],
            category=ProductCategory.objects.get(id=request.POST['categoria']),
            unitPrice=request.POST['price']
        )
        prodinv=Warehouse.objects.create(
            description = request.POST['desc'],
            product = product,
            quantity = int(request.POST['qty'])
        )
    return redirect('/admin/edit')
def editProd(request,prodId):
    if request.method=='POST':
        obj = Product.objects.filter(id=prodId).update(
            description=request.POST['prod'],
            category=ProductCategory.objects.get(id=request.POST['categoria']),
            unitPrice=request.POST['price']
        )
        objWare = Warehouse.objects.get(product=prodId)
        objWare.quantity= request.POST['qty']
        objWare.description= request.POST['desc']
        objWare.save()
        return redirect('/admin/edit')
    if request.method=='GET':
        context ={
            'user': User.objects.get(id=request.session['logged_user']),
            'product': Warehouse.objects.get(product=Product.objects.get(id=prodId)),
            'categoria': ProductCategory.objects.all()
        }
        orders=Cart.objects.filter(status="C")
        if orders:    
            context['orders']=orders 
        return render(request, 'admin/editP.html', context)
def deleteProdAdmin(request,prodId ):
    prod=Product.objects.get(id=prodId)
    prod.delete()
    return redirect ('/admin/edit')
def userAdmin(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please Register or Log In")
        return redirect("/")
    context ={
        'users': User.objects.all(),
        'profile': Profile.objects.all(),
        'categoria': ProductCategory.objects.all()
    }
    orders=Cart.objects.filter(status="C")
    if orders:    
        context['orders']=orders 
    return render(request, 'admin/user.html', context)
def createUserAdmin(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please Register or Log In")
        return redirect("/")
    if request.method=='POST':
        errors=User.objects.userAdminValidator(request.POST)
        if errors:
            for error , value in errors.items():
                messages.error(request,value)
            return redirect(f'/admin/user')
        usr=User.objects.create(
            firstName=request.POST['firstName'],
            lastName=request.POST['lastName'],
            email=request.POST['email'],
            password=request.POST['pass'],
            profileId=Profile.objects.get(id=request.POST['perfilId'])
        )
        return redirect('/admin/user')
def editUserAdmin (request,usrId):
    if 'logged_user' not in request.session:
        messages.error(request, "Please Register or Log In")
        return redirect("/")
    if request.method=='POST':
        errors=User.objects.userAdminValidator(request.POST)
        if errors:
            for error , value in errors.items():
                messages.error(request,value)
            return redirect(f'/admin/user')
    if request.method=='GET':
        content={
            'user': User.objects.get(id=usrId),
            'profile': Profile.objects.all()
        }
        orders=Cart.objects.filter(status="C")
        if orders:    
            content['orders']=orders 
        return render(request,'admin/editU.html', content)
    if request.method=='POST':
        hash_pw=bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt()).decode()
        User.objects.filter(id=usrId).update(
            firstName= request.POST['firstName'],
            lastName=request.POST['lastName'],
            email=request.POST['email'],
            password=hash_pw,
            profileId= Profile.objects.get(id=request.POST['perfilId'])
        )
        return redirect('/admin/user')
def deleteUserAdmin(request,usrId):
    userD=User.objects.get(id=usrId)
    userD.delete()
    return redirect('/admin/user')
def deliveryAdmin(request):
    onj=Cart.objects.exclude(status="O").order_by("-updatedAt")
    context = { 
        'user': User.objects.get(id=request.session['logged_user']),
        'allOrders': onj
    }
    orders=Cart.objects.filter(status="C")
    if orders:    
        context['orders']=orders       
    return render (request,'admin/delivery.html', context)
def cartAdmin(request, idCart):
    context={
        'order': Cart.objects.get(id=idCart)
    }
    orders=Cart.objects.filter(status="C")
    if orders:    
        context['orders']=orders 
    return render (request,'admin/order.html',context)
def cancelOrder(request, idCart):
    Cart.objects.filter(id=idCart).update(
        status="X"
    )
    return redirect('/admin/delivery')
def shipOrder(request, idCart):
    Cart.objects.filter(id=idCart).update(
        status="S"
    )
    return redirect('/admin/delivery')
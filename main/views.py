from typing import cast
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import User,Profile, Address, Product, ProductCategory, Warehouse, SalesOrder
from django.conf import settings
import bcrypt

from main import models

# Create your views here.
def loginIndex(request):
    return render(request,'login.html')
def createUser (request):
    if request.method=='POST':
      #  errors=User.objects.userValidator(request.POST)
        # if len(errors)>0:
        #     for key,value in errors.items():
                
        #         messages.error(request,value)
        #     return redirect('/')
        hash_pw=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        profileUser=Profile.objects.get(id=2)
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
        # errors=User.objects.loginValidator(request.POST)
        # if len(errors)>0:
        #     for key,value in errors.items():
                
        #         messages.error(request,value)
        #     return redirect('/')
        user=User.objects.filter(email=request.POST['usrEmail'])
        if user:
            log_user=user[0]
            if bcrypt.checkpw(request.POST['usrPass'].encode(), log_user.password.encode()):
                request.session['logged_user']=log_user.id
                return redirect('/home')
           # messages.error(request,"Email/Password incorrect")
    return redirect('/')
def homeIndex(request):
    user=User.objects.get(id=request.session['logged_user'])
    
    context = {'google_api_key': settings.GOOGLE_API_KEY,
                'user': user,
                'direcciones': Address.objects.filter(user__id=request.session['logged_user']),
                'products': Warehouse.objects.filter(quantity__gte=0)
    }
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
def adminIndex(request):
    context = { 'user': User.objects.get(id=request.session['logged_user'])
                
    }
    return render (request,'admin/admin.html', context)
def editIndex(request):
    context ={
        'user': User.objects.get(id=request.session['logged_user']),
        'products': Warehouse.objects.all(),
        'categoria': ProductCategory.objects.all()
    }
    return render(request, 'admin/edit.html', context)
def createProduct(request):
    if request.method=='POST':
        product = Product.objects.create(
            description = request.POST['producto'],
            category=ProductCategory.objects.get(id=request.POST['categoria'])
        )
        prodinv=Warehouse.objects.create(
            description = request.POST['desc'],
            idProduct = product,
            quantity = int(request.POST['qty']) 
        )
    return redirect('/admin/edit')
def editProd(request,prodId):
    
    if request.method=='POST':
        obj = Product.objects.filter(id=prodId).update(
            description=request.POST['prod'],
            category=ProductCategory.objects.get(id=request.POST['categoria']),

            
        )
        objWare = Warehouse.objects.get(idProduct=prodId)
        objWare.quantity= request.POST['qty']
        objWare.save()
        return redirect('/admin/edit')
    if request.method=='GET':
        context ={
            'user': User.objects.get(id=request.session['logged_user']),
            'product': Warehouse.objects.get(idProduct=Product.objects.get(id=prodId)),
            'categoria': ProductCategory.objects.all()
        }
        return render(request, 'admin/editP.html', context)
def userAdmin(request):
    context ={
        'users': User.objects.all(),
        'profile': Profile.objects.all(),
        'categoria': ProductCategory.objects.all()
    }
    return render(request, 'admin/user.html', context)
def createUserAdmin(request):
    if request.method=='POST':
        usr=User.objects.create(
            firstName=request.POST['firstName'],
            lastName=request.POST['lastName'],
            email=request.POST['email'],
            password=request.POST['pass'],
            profileId=Profile.objects.get(id=request.POST['perfilId'])
        )
        return redirect('/admin/user')
def editUserAdmin (request,usrId):
    if request.method=='GET':
        content={
            'user': User.objects.get(id=usrId),
            'profile': Profile.objects.all()
        }
        
        return render(request,'admin/editU.html', content)
    if request.method=='POST':
        User.objects.filter(id=usrId).update(
            firstName= request.POST['firstName'],
            lastName=request.POST['lastName'],
            email=request.POST['email'],
            password=request.POST['pass'],
            profileId= Profile.objects.get(id=request.POST['perfilId'])
        )
        return redirect('/admin/user')
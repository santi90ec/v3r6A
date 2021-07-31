from django.shortcuts import redirect, render
from django.contrib import messages
from .models import User,Profile, Address
from django.conf import settings
import bcrypt

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
                'direcciones': Address.objects.filter(user__id=request.session['logged_user'])
    }
    if user.profileId.id == 1:
        return render(request,'user.html' , context)
    if user.profileId.id == 2:
        return render(request,'admin.html', context)
def logout(request):
    request.session.flush()
    return redirect('/')
def createAddress(request):
    if request.method=='POST':
        add=Address.objects.create(
            description=request.POST['txtCasa'],
            lat=request.POST['id_lat'],
            lon=request.POST['id_lng'],
            user=User.objects.get(id=request.session['logged_user'])
        )
        return redirect('/home')
def MasterpageIndex(request):
    return render (request,'prueba.html')
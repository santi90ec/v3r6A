from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
urlpatterns = [
    path('',views.loginIndex),
    path('login',views.login),
    path('register',views.createUser),
    path('home',views.homeIndex),
    path('home/addAddress',views.createAddress)
]

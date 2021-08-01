from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
urlpatterns = [
    path('',views.loginIndex),
    path('login',views.login),
    path('register',views.createUser),
    path('home',views.homeIndex),
    path('home/addAddress',views.createAddress),
    path('admin/index',views.adminIndex),
    path('admin/edit',views.editIndex),
    path('admin/edit/create',views.createProduct),
    path('admin/edit/<int:prodId>',views.editProd),
    path('admin/user', views.userAdmin),
    path('admin/user/create', views.createUserAdmin),
    path('admin/user/<int:usrId>', views.editUserAdmin),

]

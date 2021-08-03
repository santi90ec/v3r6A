from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
urlpatterns = [
    path('',views.loginIndex),
    path('login',views.login),
    path('logout',views.login),
    path('register',views.createUser),
    path('home',views.homeIndex),
    path('home/cart/<int:idProd>',views.addProduct2Cart),
    path('home/cart',views.cart),
    path('home/cart/delete',views.deleteCart),
    path('home/cart/order',views.orderCart),
    path('home/profile',views.profile),
    path('home/profile/deleteAdd/<int:idAdd>',views.deleteAddress),
    path('home/addAddress',views.createAddress),
    path('admin/index',views.adminIndex),
    path('admin/edit',views.editIndex),
    path('admin/edit/create',views.createProduct),
    path('admin/edit/<int:prodId>',views.editProd),
    path('admin/edit/<int:prodId>/delete',views.deleteProdAdmin),
    path('admin/user', views.userAdmin),
    path('admin/user/create', views.createUserAdmin),
    path('admin/user/<int:usrId>', views.editUserAdmin),
    path('admin/user/<int:usrId>/delete', views.deleteUserAdmin),
    path('admin/delivery', views.deliveryAdmin),
    path('admin/delivery/<int:idCart>', views.cartAdmin),
    path('admin/delivery/<int:idCart>/cancel', views.cancelOrder),
    path('admin/delivery/<int:idCart>/ship', views.shipOrder),

]

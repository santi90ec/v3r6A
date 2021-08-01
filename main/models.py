from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def userValidator(self,postData):
        errors={}
        if len(postData['firstName'])<2 or len(postData['lastName'])<2 or len(postData['email'])<2 or len(postData['password'])<2:
            errors['Empty']="None field must be empty"

        prev_usr=User.objects.filter(email=postData['email'])
        if len(prev_usr) >=1:
            errors['exists']="Email address already exists" 
        if not EMAIL_REGEX.match(postData['email']):
            errors['emailValido']="Invalid Mail"
        if (len(postData['password'])<8)  :
            errors['pass']="Password not strong enough"
        if (len(postData['confirpassword'])<8 or (postData['password']!=postData['confirpassword'])):
            errors['confirpassword']="La contraseña es invalido o no coinciden"
        return errors
    def loginValidator(self,postData):
        errors={}
        if len(postData['usrEmail'])<2 or len(postData['usrPass'])<2:
            errors['login']="Username / Mail can not be empty"
        return errors
# Create your models here.
class Profile(models.Model):
    profileName=models.CharField(max_length=40)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)

class User(models.Model):
    firstName=models.CharField(max_length=40)
    lastName=models.CharField(max_length=40)
    email=models.EmailField()
    password=models.CharField(max_length=40)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    profileId=models.ForeignKey(Profile, related_name="user_profile", on_delete=models.CASCADE)
    objects = UserManager()
class Address(models.Model):
    description = models.CharField(max_length=100)
    lat = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="user_address", on_delete=models.CASCADE)
class ProductCategory(models.Model):
    category = models.CharField(max_length=45)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
class Product(models.Model):
    description = models.CharField(max_length=100)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    category= models.ForeignKey(ProductCategory, related_name="product_category", on_delete=models.CASCADE)
    unitPrice=models.DecimalField(max_digits=10,decimal_places=2, default=0.00)
class Warehouse(models.Model):
    description = models.CharField(max_length=45)
    idProduct= models.ForeignKey(Product, related_name="product_inventory", on_delete=models.CASCADE)
    createdAt=models.DateTimeField(auto_now_add=True)
    quantity=models.SmallIntegerField()
    updatedAt=models.DateTimeField(auto_now=True)
class SalesOrder(models.Model):
    status = models.CharField(max_length=1)
    idUser = models.ForeignKey(User, related_name="user_order", on_delete=models.CASCADE)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
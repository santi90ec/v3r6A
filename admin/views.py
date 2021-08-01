from django.shortcuts import render
from main.models import User,Profile,Address 
def rootIndex(request):
    return render(request,'adminmasterPage.html')
# Create your views here.

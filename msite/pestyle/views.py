from django.shortcuts import render
from django.contrib import auth
# Create your views here.
#from pestyle.forms import *
from pestyle.models import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def main_page(request):
    image = User.objects.get(pk=User.objects.count()).avatar
    image1 = User.objects.get(pk=2).avatar
    return render(request, 'base.html', {'data': "lolol", 'image':image, 'image1':image1})

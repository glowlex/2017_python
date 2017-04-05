from django.shortcuts import render
from django.contrib import auth
# Create your views here.
#from pestyle.forms import *
from pestyle.models import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def main_page(request):
    return render(request, 'base.html', {'data': "lolol"})

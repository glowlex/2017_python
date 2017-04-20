from django.shortcuts import render
from django.contrib import auth
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def main_page(request):
    log_form = User_Login_Form(request.POST or None)
    reg_form = User_Registration_Form(request.POST or None)
    if request.method == 'POST' and log_form.is_valid():
        email = log_form.cleaned_data.get('email', None)
        password = log_form.cleaned_data.get('password', None)
        user = auth.authenticate(email=email, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return redirect('/')
    reg_form = User_Registration_Form(request.POST or None)
    if request.method == 'POST' and reg_form.is_valid():
        email = reg_form.cleaned_data.get('email', None)
        password = reg_form.cleaned_data.get('password', None)
        user = auth.authenticate(email=email, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return redirect('/')
    return render(request, 'main.html',  {'log_form': log_form, 'reg_form':reg_form})

from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def main_page(request):
    log_form = User_Login_Form(request.POST or None)
    if request.method == 'POST' and log_form.is_valid():
        email = log_form.cleaned_data.get('email', None)
        password = log_form.cleaned_data.get('password', None)
        user = auth.authenticate(email=email, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return redirect('look_choice/')

    reg_form = User_Registration_Form(request.POST or None)
    if request.method == 'POST' and reg_form.is_valid():
        email = reg_form.cleaned_data.get('email', None)
        name = reg_form.cleaned_data.get('name')
        sex = reg_form.cleaned_data.get('sex')
        city = reg_form.cleaned_data.get('city')
        reg_form.ValidationError('user data is corupted')
        password = reg_form.cleaned_data.get('password', None)
        birthday = reg_form.cleaned_data.get('birthday', None)
        last_name = reg_form.cleaned_data.get('last_name', None)
        avatar = None
        if 'avatar' in request.FILES:
            avatar=handle_uploaded_file(request)

        user = User.objects.create_user(email, name, sex, city, password, last_name, birthday, avatar)
        user = auth.authenticate(user)
        if user and user.is_active:
            auth.login(request, user)
            return redirect('look_choice/')

    return render(request, 'main.html',  {'log_form': log_form, 'reg_form':reg_form})



@login_required
def look_choice(request):
    #TODO: сменить таблицу
    return render(request, 'look_choice.html',  {})



#TODO отправув json
@login_required
def get_looks(request):
    looks = Look.objects.filter(user=request.user)[:10]

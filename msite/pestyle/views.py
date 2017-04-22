from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def main_page(request):
    if request.user.is_authenticated:
        return redirect('/look_choice/')
    log_form = User_Login_Form(request.POST or None)
    #TODO при наличии 2 форм, нажимая на регу условие во второй не срабатывает,
    # но при обновлении форма логина делает аунтефикацию и логин
    if request.method == 'POST' and log_form.is_valid() and log_form.has_changed():
        email = log_form.cleaned_data.get('email', None)
        password = log_form.cleaned_data.get('password', None)
        user = auth.authenticate(email=email, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return redirect('/look_choice/')

    reg_form = User_Registration_Form(request.POST or None)
    if request.method == 'POST' and reg_form.is_valid() and reg_form.has_changed():
        user = reg_form.save()
        if 'avatar' in request.FILES:
            user.set_avatar(request.FILES['avatar'])
        #TODO с .save() не аунтефицирует далее хоть фактически делает логин
        #user= auth.authenticate(user)
        if user:# and user.is_active:
            print('reg form login work')
            auth.login(request, user)
            return redirect('/look_choice/')

    return render(request, 'main.html',  {'log_form': log_form, 'reg_form':reg_form})





@login_required
def logout(request):
    logout(request)

'''    if request.method == 'POST':
        prof_form = User_Profile_Form(request.POST, request.FILES)
        if prof_form.is_valid():
            user = prof_form.save()
            auth.login(request, user)
    else:
        prof_form = User_Profile_Form(None, instance=request.user)

    return render(request, 'look_choice.html', {'prof_form':prof_form})'''


@login_required
def look_choice(request):
    prof_form = User_Profile_Form(request.POST or None,  instance=request.user)
    if request.method == 'POST' and prof_form.is_valid() and prof_form.has_changed():
        user=prof_form.save()
        #TODO загрузка файлов
        if 'avatar' in request.FILES:
            user.set_avatar(request.FILES['avatar'])
        #TODO user= auth.authenticate(user)
        if user:# and user.is_active:
            auth.login(request, user)
    return render(request, 'look_choice.html', {'prof_form':prof_form})



#TODO отправув json
@login_required
def get_looks(request):
    looks = Look.objects.filter(user=request.user)[:10]

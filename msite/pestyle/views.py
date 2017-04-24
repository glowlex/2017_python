from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Prefetch, prefetch_related_objects, Q
from django.template.response import TemplateResponse
import json

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
    last = int(request.GET.get('last', None))
    looks = {}
    rtype = request.GET.get('type', False)
    tmp=[]
    if rtype == 's':
        looks = Look_suggestions.objects.prefetch_related(Prefetch(
    'items',
     queryset=Item.objects.all(),
     to_attr='tp')
    ).filter(user=request.user)[last:last+7]
    elif rtype == 'c':
        looks = Look.objects.prefetch_related(Prefetch(
    'items',
     queryset=Item.objects.all(),
     to_attr='tp')
    ).filter(user=request.user)[last:last+7]

    for l in looks:
        tmp.append({"pk":l.pk, 'like':l.like if rtype=='s' else True, "items": json.loads(serializers.serialize('json', l.tp, fields=('item_type', 'photo')))})
    #TODO норм жсон без двойного парса на клиенте или ^ конструкции
    return JsonResponse(tmp, safe=False)



@login_required
def get_items(request):
    itype = json.loads(request.GET.get('itype', None))
    queries = [Q(item_type=i) for i in itype]
    query = queries.pop()
    for item in queries:
        query |= item
    items = Item.objects.filter(query)
    print(items)
    return JsonResponse(serializers.serialize('json',items,  fields=('item_type', 'photo')), safe=False)



@login_required
def item_window(request):
    item_form = Item_Form(request.POST or None)
    return TemplateResponse(request, 'item.html', {'item_form':item_form})



@login_required
def like_look(request):
    lid = int(request.GET.get('look_id', None))
    up = request.GET.get('up', False)
    if up =='false':
        up = False
    else:
        up= True
    look = Look_suggestions.objects.get(pk=lid)
    if request.user.pk==look.user.pk:
        look.set_like(up)
    return JsonResponse({'status': 'true', 'look_id':lid,})

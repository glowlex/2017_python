from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.db.models import Prefetch, prefetch_related_objects, Q
from django.template.response import TemplateResponse
import json
from .lists import *
from django.core.exceptions import EmptyResultSet, ObjectDoesNotExist

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
    if not request.method == 'GET':
        return HttpResponseForbidden()
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
    return HttpResponse(json.dumps(tmp), content_type = "application/json")



@login_required
def get_items(request):
    if not request.method == 'GET':
        return HttpResponseForbidden()
    itype = json.loads(request.GET.get('itype', None))
    queries = [Q(item_type=i) for i in itype]
    query = queries.pop()
    for item in queries:
        query |= item
    items = Item.objects.filter(Q(user=request.user.id) & query).order_by('-pk')
    return HttpResponse(serializers.serialize('json', items,), content_type = "application/json")



@login_required
def get_item_window(request):
    if not request.method == 'GET':
        return HttpResponseForbidden()
    item_form = Item_Form(request.POST or None,
     initial={'item_type':ITEM_TYPE_LIST[0][0],
             'style':STYLE_LIST[0][0],
             'color':COLOR_LIST[0][0],
             'season':SEASON_LIST[0][0],
             'temperature':TEMPERATURE_LIST[0][0],
             'sky':SKY_LIST[0][0],
             })
    return TemplateResponse(request, 'item.html', {'item_form':item_form})

@login_required
def set_item(request):
    item_id=request.POST.get('item_id')
    item = Item.objects.get(pk=item_id) if item_id else None
    if request.method != 'POST' or (item and item.user_id!=request.user.id):
        return HttpResponseForbidden()
    if item_id:
        item = Item_Form(data=request.POST, instance=item).save()
    else:
        item = Item_Form(request.POST, request.FILES, user_id=request.user.id,
     item_id=item_id).save()
    #1 объект не сереализуется и делаем костыль
    item = Item.objects.filter(pk=item.id)
    return HttpResponse(serializers.serialize('json', item, ), content_type = "application/json")


@login_required
def delete_item(request):
    item_id = request.POST.get('item_id')
    item = None
    try:
        item = Item.objects.get(pk=item_id)
    except ObjectDoesNotExist:
        return HttpResponseForbidden()
    if request.method != 'POST' or (item and item.user_id!=request.user.id):
        return HttpResponseForbidden()
    item.delete()
    return JsonResponse({'status': 'ok',})


@login_required
def like_look(request):
    lid = int(request.POST.get('look_id', None))
    #TODO переделать. так, чтобы работало удаление избранных
    try:
        look = Look_suggestions.objects.get(pk=lid)
    except ObjectDoesNotExist:
        look = Look.objects.get(pk=lid)
        look.delete()
    if not request.method == 'POST' or request.user.id != look.user.id:
        return HttpResponseForbidden()
    up = request.POST.get('up', False)
    if up =='false':
        up = False
    else:
        up= True
    if request.user.id==look.user.id and isinstance(look, Look_suggestions):
        look.set_like(up)
    return JsonResponse({'status': 'ok', 'look_id':lid,})

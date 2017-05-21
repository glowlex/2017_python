
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
import datetime
from .scripts.weather import Weather
from .scripts.gen_looks import Looks



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
    ll = Looks(request.user)
    ll.generate_looks()
    weather = Weather().weather_dictionary(request.user.city)
    return render(request, 'look_choice.html', {'prof_form':prof_form, 'weather':weather})



#TODO отправув json
@login_required
def get_looks(request):
    if not request.method == 'GET':
        return HttpResponseForbidden()
    last = int(request.GET.get('last', None))
    looks = {}
    rtype = request.GET.get('type', False)
    tmp=[]
    try:
        if rtype == 's':
            looks = Look_suggestions.objects.prefetch_related(Prefetch(
        'items',
         queryset=Item.objects.all(),
         to_attr='tp')
        ).filter(user=request.user).filter(like=False)[last:last+7]
        elif rtype == 'c':
            looks = Look.objects.prefetch_related(Prefetch(
        'items',
         queryset=Item.objects.all(),
         to_attr='tp')
        ).filter(user=request.user)[last:last+7]
    except DoesNotExist:
        return JsonResponse({'status': 'ok',})

    for l in looks:
        tmp.append({"pk":l.pk, 'like':l.like if rtype=='s' else True, "items": json.loads(serializers.serialize('json', l.tp, fields=('item_type', 'photo')))})
    #TODO норм жсон без двойного парса на клиенте или ^ конструкции
    return HttpResponse(json.dumps(tmp), content_type = "application/json")



@login_required
def get_items(request):
    if not request.method == 'GET':
        return HttpResponseForbidden()
    #itype = json.loads(request.GET.get('itype', None))
    #queries = [Q(item_type=i) for i in itype]
    #query = queries.pop()
    #for item in queries:
        #query |= item  '''& query'''
    items = Item.objects.filter(Q(user=request.user.id)).order_by('-pk')
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
    up = request.POST.get('up', True)
    if up =='false':
        up = False
    else:
        up= True
    #TODO переделать. так, как в 2 таблицах ищет ид из одной из них
    if up:
        try:
            look = Look_suggestions.objects.get(pk=lid)
        except ObjectDoesNotExist:
            return HttpResponseForbidden()
    else:
        try:
            look = Look.objects.get(pk=lid)
            look.delete()
        except ObjectDoesNotExist:
            return HttpResponseForbidden()
    if not request.method == 'POST' or request.user != look.user:
        return HttpResponseForbidden()
    #TODO поправить nl и отдавать объект
    if request.user.id==look.user.id and isinstance(look, Look_suggestions):
        nl = Look.create_look(look.user, look.style, look.items.all())
        look.delete()
    return JsonResponse({'status': 'ok', 'look_id':lid,})

@login_required
def new_look(request):
    ids = json.loads(request.POST.get('ids', None))
    for i in ids:
        if Item.objects.get(id=int(i)).user != request.user:
            return HttpResponseForbidden()
    #TODO пока так стиль
    look = Look.create_look(request.user, STYLE_LIST[0][0], ids)
    l = Look.objects.prefetch_related(Prefetch(
    'items',
     queryset=Item.objects.all(),
     to_attr='tp')
    ).get(pk=look.pk)
    tmp = []
    tmp.append({"pk":l.pk, 'like': True, "items": json.loads(serializers.serialize('json', l.tp, fields=('item_type', 'photo')))})
    return HttpResponse(json.dumps(tmp), content_type = "application/json")



@login_required
def set_event(request):
    etype = request.POST.get('etype')
    date = json.loads(request.POST.get('date'))
    if request.method != 'POST' and not date and not etype:
        return HttpResponseForbidden()
    try:
        date = datetime.datetime(year=date['year'], month=date['month'], day=date['day'])
        event = Event.create_event(user=request.user, date=date, event_type=etype)
    except:
        return HttpResponseForbidden()
    event = Event.objects.filter(pk=event.id)
    return HttpResponse(serializers.serialize('json', event, fields=('event_type', 'date')), content_type = "application/json")



@login_required
def delete_event(request):
    pass




@login_required
def get_calendar(request):
    if not request.method == 'GET':
        return HttpResponseForbidden()
    calendar = Event.objects.filter(user=request.user)
    r = {'calendar':json.loads(serializers.serialize('json', calendar, fields=('event_type', 'date'))), 'styles': STYLE_LIST}
    return JsonResponse(r)







#e

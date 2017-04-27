from django.core.management.base import BaseCommand, CommandError
from pestyle.models import *
from django.utils.crypto import get_random_string
from random import randint
from datetime import datetime, timedelta
from pestyle.lists import *
from requests import get
from django.core.files import File


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.test=options.get('test', False)
        if(self.test):
            self.pic = File(open(settings.BASE_DIR+'/pestyle/static/images'+'/other/1.png', 'rb'))

        if(User.objects.filter(email='test@test.ru').count()==0):
            User.objects.create_user(name='test', last_name='testovich', email ='test@test.ru',
                    sex ='F', birthday =datetime.now(), city=55, password='1', avatar=self.get_avatar(60, 60))
        self.users(*args, **options)
        print("user complete")
        self.items(*args, **options)
        print("item complete")
        self.looks(*args, **options)
        print("looks complete")
        self.looks_s(*args, **options)
        print("looks_s complete")
        self.events(*args, **options)
        print("events complete")


    def users(self, *args, **options):
        uscount = User.objects.all().count()
        for i in range(uscount, uscount+options.get('users', 3)):
            name = "UserN_"+str(i)+get_random_string(length=3)
            last_name = None if randint(1, 2) == 1 else get_random_string(length=24)
            email = "a" + str(i) + "@aaaa.go"
            sex = 'F'
            birthday = datetime.now() - timedelta(days=randint(366*10, 366*50))
            city = randint(0, 10**7)
            password =get_random_string(length=10)


            User.objects.create_user(name=name, last_name=last_name, email =email,
            sex =sex, birthday =birthday, city=city, password=password, avatar =self.get_avatar(60, 60))



    def items(self, *args, **options):
        for _ in range(options.get('items', 1000)):
            user = User.objects.get(id=randint(1, User.objects.all().count()))
            item_type = ITEM_TYPE_LIST[randint(0, len(ITEM_TYPE_LIST)-1)][0]
            style = STYLE_LIST[randint(0, len(STYLE_LIST)-1)][0]
            color = COLOR_LIST[randint(0, len(COLOR_LIST)-1)][0]
            season = SEASON_LIST[randint(0, len(SEASON_LIST)-1)][0]
            temperature = TEMPERATURE_LIST[randint(0, len(TEMPERATURE_LIST)-1)][0]
            sky = SKY_LIST[randint(0, len(SKY_LIST)-1)][0]

            Item.create_item(user =user, item_type =item_type, photo =self.get_avatar(300, 300), style =style,
    		 color =color, season =season, temperature =temperature, sky =sky,)



    def looks(self, *args, **options):
        for _ in range(options.get('looks', 30)):
            #сделать переопределение в листах, что к чему
            user = User.objects.get(pk=randint(1, User.objects.all().count()))
            style = ('C','B','S','P',)[randint(0,3)]
            body = ('dress', 'blouse', 'Tshirt')
            pants = ('pants', 'skirt')
            outerwear = ('outerwear',)
            accessory = ('bag', 'cap', 'glasses')
            shoes = ('Sneakers', 'Shoes', 'Boots', 'footwear')

            dickt = {'body':body, 'pants':pants, 'outerwear':outerwear,
            'accessory':accessory, 'shoes':shoes}

            all_items = user.item_set.all()

            def pick(items, name, dickt):
                i = None
                j=10
                while not i and j>0:
                    item_type = dickt[name][randint(0,len(dickt[name])-1)]
                    i = items.filter(item_type=item_type)
                    if i:
                        i = i[randint(0, i.count()-1)]
                    j-=1
                return i

            item_dict = {}
            for key in dickt:
                itm = pick(all_items, key, dickt)
                if itm:
                    item_dict[key] = itm

            if len(item_dict.values())<2:
                continue

            Look.create_look(user, style, item_dict.values())



    def looks_s(self, *args, **options):
        for _ in range(options.get('looks_suggestions', 30)):
            #сделать переопределение в листах, что к чему
            user = User.objects.get(pk=randint(1, User.objects.all().count()))
            style = ('C','B','S','P',)[randint(0,3)]
            body = ('dress', 'blouse', 'Tshirt')
            pants = ('pants', 'skirt')
            outerwear = ('outerwear',)
            accessory = ('bag', 'cap', 'glasses')
            shoes = ('Sneakers', 'Shoes', 'Boots', 'footwear')

            dickt = {'body':body, 'pants':pants, 'outerwear':outerwear,
            'accessory':accessory, 'shoes':shoes}

            all_items = user.item_set.all()

            def pick(items, name, dickt):
                i = None
                j=10
                while not i and j>0:
                    item_type = dickt[name][randint(0,len(dickt[name])-1)]
                    i = items.filter(item_type=item_type)
                    if i:
                        i = i[randint(0, i.count()-1)]
                    j-=1
                return i

            item_dict = {}
            for key in dickt:
                itm = pick(all_items, key, dickt)
                if itm:
                    item_dict[key] = itm

            if len(item_dict.values())<2:
                continue

            Look_suggestions.create_look(user, style, item_dict.values())



    def events(self, *args, **options):
        for _ in range(options.get('events', User.objects.all().count()*30)):
            user = User.objects.get(pk=randint(1, User.objects.all().count()))
            date = datetime.now() + timedelta(days=randint(0, 10))
            event_type = STYLE_LIST[randint(0, len(STYLE_LIST)-1)][0]
            description = None if randint(0,2)==1 else get_random_string(length=randint(16, 256))
            name = get_random_string(length=randint(6, 32))

            Event.create_event(user=user, date=date, event_type=event_type, name=name, description=description)

    def get_avatar(self, w, h):
        if(self.test):
            return self.pic
        r = get("http://lorempixel.com/%s/%s/" %(w, h))
        f = open("/tmp/1.jpg", 'wb')
        f.write(r.content)
        reopen = open('/tmp/1.jpg', 'rb')
        return  File(reopen)

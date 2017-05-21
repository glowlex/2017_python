from .weather import *
import datetime
from pestyle.models import *
from pestyle.lists import *
import random
from django.db.models import Q


class Looks():
    city_id = 524894
    def __init__(self, current_user):
        self.current_user = current_user
        self.weather = Weather().weather_dictionary(self.city_id)
        self.dict_of_items = {}
        self.num_of_look = 0
        self.cur_event = self.get_event()


    def prep_dict(self):
        for dictt in TYPES_OF_ITEMS.keys():
            self.dict_of_items[dictt] = []

    def season(self):
        date = datetime.date.today()
        for seas in SEASONS.keys():
            if SEASONS[seas].count(date.month) != 0:
                return seas

    def get_type(self, item):
        for dictt in TYPES_OF_ITEMS.keys():
            if item.item_type in TYPES_OF_ITEMS[dictt]:
                return dictt
        return None

    def get_event(self):
        cur_event = Event.objects.filter(user=self.current_user.id).filter(date=datetime.date.today())
        cur_event = cur_event.first()
        if cur_event == None:
            return 'C'
        else:
            return cur_event.event_type

    def get_weather(self):
        for temp in TEMPERATURE_ID.keys():
            if (self.weather['temp'] >= TEMPERATURE_ID[temp][0]) and (self.weather['temp'] <= TEMPERATURE_ID[temp][1]):
                return temp
        return 'all'

    def get_items(self):
        sea = self.season()
        list_of_items = Item.objects.filter(user=self.current_user)\
            .filter(Q(season=sea)|Q(season='WY'))\
            .filter(Q(temperature=self.get_weather())|Q(temperature='all'))\
            .exclude(item_type='umbrella') \
            .filter(style=self.cur_event)
        return list_of_items

    def spliting_by_types(self):
        self.prep_dict()
        for item in self.get_items():
            type = self.get_type(item)
            if type:
                self.dict_of_items[type].append(item)
        return self.dict_of_items
#конец формирования словаря из названия вещи и списка самих вещей_______________________________________________________


    def check(self, item):
        if item.item_type == TYPES_OF_ITEMS['body'][0]:
            return True
        else:
            return False

    def need_item(self, item, main_color):
        if len(item)==0:
            return None
        element = item[random.randint(0, len(item)-1)]
        num=0
        while num <= (len(item)+10):
            num += 1
            if KOLOR_DIKT.get(main_color):
                if (element.color in KOLOR_DIKT[main_color]) or (KOLOR_DIKT[main_color] == 'all'):
                    element = item[random.randint(0, len(item))-1]
                    return element
            else:
                return None


    def get_other_items(self, color, num):
        cur_list = []
        for i in range(num, 6):
            item = self.dict_of_items[LIST_OF_TYPES[i]]
            prov = self.need_item(item, color)
            if prov != None:
                cur_list.append(prov)
        if len(cur_list) < 4:
            return None
        else:
            return cur_list

        return cur_list

    def write_items(self, main_body):
        dres = self.check(main_body)
        if dres:
            num = 2
        else:
            num = 1
        for j in range(0, 3):
            mas_of_other_items = self.get_other_items(main_body.color, num)
            if mas_of_other_items:
                mas_of_other_items.insert(0, main_body)
                print(mas_of_other_items)
                Look_suggestions.create_look(self.current_user, self.cur_event, mas_of_other_items)
                self.num_of_look += 1
        return mas_of_other_items

    def generate_looks(self):
        self.spliting_by_types()
        current_budy = self.dict_of_items[LIST_OF_TYPES[0]]
        for item in current_budy:
            self.write_items(item)
        if (self.num_of_look == 0) and (self.cur_event != 'C'):
            self.cur_event = 'C'
            self.generate_looks()
# Запись в БД сгенерированных луков_____________________________________________________________________________________






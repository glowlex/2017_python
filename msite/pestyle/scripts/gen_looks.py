from .weather import *
import datetime
from msite.pestyle.models import *
from msite.pestyle.lists import *


class Looks():
    num_of_look = 0
    current_user = ''
    city_id = 524894
    dict_of_items = {}
    def __int__(self, city_id, current_user):
        self.city_id = city_id
        self.current_user = current_user

    def prep_dict(self):
        for dictt in TYPES_OF_ITEMS.keys():
            self.dict_of_items[dictt] = []

    def season(self):
        date = datetime.date.today()
        for seas in seasons.keys():
            if seasons[seas].count(date._month) != 0:
                return seas
    #seasons нужно додумать

    def get_type(self, item):
        for dictt in TYPES_OF_ITEMS.keys():
            if item[2] == dictt:
                return dictt

    def get_items(self):
        weather = Weather.weather_dictionary(self.city_id)
        sea = self.season()
        cur_event = Event.objects.filter(user=self.current_user).filter(date=datetime.date)
        list_of_items = Item.objects.filter(user=self.current_user)\
            .filter(season=sea)\
            .filter(temperature=weather['weather_id'])\
            .filter(style=cur_event[1])\
            .filter(last_date__lte=datetime.date.today())
        return list_of_items

    def spliting_by_types(self):
        self.prep_dict()
        for item in self.get_items():
            self.dict_of_items[self.get_type(item)].append(item)
#конец формирования словаря из названия вещи и списка самих вещей_______________________________________________________


    def check(self, item):
        if item.item_type == TYPES_OF_ITEMS['body'][0]:
            return True
        else:
            return False

    def get_other_items(self, color, num):
        cur_list = []
        for item in self.dict_of_items[LIST_OF_TYPES[num]]:
            if (item.color in KOLOR_DIKT[color]) or (KOLOR_DIKT[color] == 'all'):
                cur_list.append(item)
                num += 1
                if num == len(LIST_OF_TYPES):
                    return cur_list

    def write_items(self, main_body):
        dres = self.check(main_body)
        if dres:
            num = 2
        else:
            num = 1
        cur_event = Event.objects.filter(user=self.current_user).filter(date=datetime.date)
        for j in range(0, 3):
            mas_of_other_items = self.get_other_items(main_body.color, num)
            self.num_of_look += 1
            mas_of_other_items.insert(0, main_body)
            for item in mas_of_other_items:
                it = Look(user= self.current_user, style= cur_event[1])
                it.item = item
                it.num_of_look = self.num_of_look
                it.date= cur_event
                it.save()
            # Запись____________________________________________________________________________________
        return mas_of_other_items

    def generate_looks(self):
        test = []
        current_budy = self.dict_of_items[LIST_OF_TYPES[0]]
        for item in current_budy:
            test.append(self.write_items(item))
            if self.num_of_look == 6:
                return test
# Запись в БД сгенерированных луков_____________________________________________________________________________________















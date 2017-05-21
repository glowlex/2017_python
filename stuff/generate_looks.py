from django.db import models

#Получаем словарь
#{ "ID_вещи", [Словарь параметров]}
#Сам словарь: [тип вещи, стиль, цвет, сезон, температура, осадки]
#Из viev приходит текущая погода и запланированные события
#Пусть погода будет в виде словаря
#Сам словарь [температура, осадки]
#Погоду нужно будет получать из XML
#Запланированные события в виде строки
#Пустая, если нет события, иначе название события#

class Look(models.Model):
    Clothes = {}
    body_str = 'платье_блузка_футболка'
    pants_str = 'брюки_юбка'
    outerwear_str = 'верхняя одежда'
    accessory_str = 'сумка_шапка_очки'
    shoes_str = 'кросовки_туфли_ботинки'
    weather = []
    style = ""
    season = ""
    dress = False
    body_item = {}
    pants_item = {}
    shoes_item = {}
    accessory_item = {}
    outerwear_item = {}
    list_of_pants = []
    list_of_shoes = []
    list_of_accessory = []
    list_of_outerwear = []
    def sort_item(self):
        for key, item in self.Clothes.items():

            if item[0] in self.body_str:
                if self.find_item(item):
                    self.body_item[key] = item

            elif item[0] in self.pants_str:
                if self.find_item(item):
                    self.pants_item[key] = item

            elif item[0] in self.outerwear_str:
                if self.find_item(item):
                    self.pouterwear_item[key] = item

            elif item[0] in self.accessory_str:
                if self.find_item(item):
                    self.accessory_item[key] = item

            elif item[0] in self.outerwear_str:
                if self.find_item(item):
                    self.outerwear_item[key] = item


    def find_item(self, item):
        if (item[4] != self.weather[0]) and (item[5] != self.weather[1]):
            return False
        elif (self.events == "")or(item[1] != self.events):
            return False
        elif item[1] != self.style:
            return False
        elif item[3] != self.season:
            return False
        else:
            return True

# Сначала мы смотрим на первую верхнюю вещь
# К ней подбираем по очереди вещи, сочетающиеся по оттенку
# Полученную структуру записываем в список
# С списке бедет находиться ключи вещей

    def new_look(self):
        for key, item in self.body_item.items():
            self.dress = False
            if item[0] == "платье":
                self.dress = True
            f = open('colors.txt', 'r')
            for line in f:
                colors = line.split(' ')
                if item[2] == colors[0]:
                    matching_colors = colors[1]
                    break
            f.close()
            if self.dress == False:
                for i in range(0, 2):
                    self.list_of_pants.append(self.Find(self.pants_item, matching_colors, self.list_of_pants))

            for i in range(0, 2):
                self.list_of_shoes.append(self.Find(self.shoes_item, matching_colors, self.list_of_shoes))
                self.list_of_accessory.append(self.Find(self.accessory_item, matching_colors, self.list_of_accessory))
                self.list_of_outerwear.append(self.Find(self.outerwear_item, matching_colors, self.list_of_outerwear))
                # Тут происходит компоновка 5-ти элементов и запись в БД


    def Find(self, dict, matching_colors, lst):
        for key, item in dict.items():
            if lst.count(key) == 0:
                if item[2] in matching_colors:
                    return key



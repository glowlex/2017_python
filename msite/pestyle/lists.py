
STYLE_LIST = (
('C', 'повседневный'),
('B', 'деловой'),
('S', 'спорт'),
('P', 'вечеринка'),
)

ITEM_TYPE_LIST =(
('', 'тип'),
('dress', 'платье'),
('blouse', 'блузка'),
('pants', 'брюки'),
('outerwear', 'верхняя одежда'),
('umbrella', 'зонт'),
('glasses', 'очки'),
('bag', 'сумка'),
('skirt', 'юбка'),
('cap', 'головной убор'),
('tshirt', 'футболка'),
('sneakers', 'кроссовки'),
('shoes', 'туфли'),
('boots', 'ботинки'),
)

#справочная инфа для фронта
body = ('dress', 'blouse', 'tshirt')
pants = ('pants', 'skirt')
outerwear = ('outerwear',)
glasses = ('cap', 'glasses')
shoes = ('sneakers', 'shoes', 'boots', 'footwear')
bag = ('bag',)

COLOR_LIST = (
('black', 'чёрный'),
('white','белый'),
('milk','молочный'),
('beige','бежевый'),
('deep_blue','синий'),
('olivaceous','оливковый'),
('deep_green','зелёный'),
('vinous','бордовый'),
('chocolate','шоколадный'),
('blue','голубой'),
('pink','розовый'),
('coral','коралловый'),
('red','красный'),
('yellow','жёлтый'),
('purple','фиолетовый'),
('gray','серый'),
)

SEASON_LIST = (
('Wn', 'зима'),
('Sp', 'весна'),
('Sm', 'лето'),
('At', 'осень'),
('SS', 'весна-лето'),
('AW', 'осень-зима'),
('WY', 'круглый год'),
)

TEMPERATURE_LIST =(
('all', 'любая'),
('dubak', "от -35 до +5"),
('prohladno', "от +5 до +15"),
('zaebok', "от +15 до +20"),
('szara', "от +20 до +35"),
)

SKY_LIST = (
('clouds', 'облачно'),
('rain', 'дождь'),
('clear', 'ясно'),
)

SEX_LIST = (
('M', 'М'),
('F', 'Ж')
)

LIST_OF_TYPES = ['body', 'pants', 'shoes', 'outerwear', 'accessory', 'bag']

TYPES_OF_ITEMS = {
    'body': ('dress', 'blouse', 'tshirt'),
    'pants': ('pants', 'skirt'),
    'shoes': ('sneakers', 'shoes', 'boots', 'footwear'),
    'outerwear' : ('outerwear'),
    'accessory':('cap', 'glasses'),
    'bag': ('bag')
}

KOLOR_DIKT = {
        'black': 'all',
        'white': 'all',
        'beige': 'all',
        'olivaceous': 'white_beige_blue_blue',
        'green': 'chocolate_gray_black_white_beige_blue',
        'burgundy': 'black_blue_green_olive_gray_white_beige_gray',
        'chocolate': 'white_beige_coral_pink_yellow_blue_green',
        'blue': 'white_beige_blue_olive_chocolate_pink_coral_yellow_purple_gray',
        'pink': 'white_beige_chocolate_blue_coral_purple_gray',
        'coral': 'white_beige_chocolate_pink_blue_blue_black',
        'red': 'black_white_gray',
        'yellow': 'blue_purple_blue',
        'purple': 'white_beige_yellow_pink_coral_gray_blue',
        'gray': 'all'
}

SEASONS = {
        'Wn': [12, 1, 2],
        'Sp': [3, 4 ,5],
        'Sm': [6, 7, 8],
        'At': [9, 10, 11],
        'SS': [3, 4, 5, 6, 7, 8],
        'AW': [9, 10, 11, 12, 1, 2],
        'WY': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
}

WEATHER_ID = {
    'clouds': [801, 804],
    'rain': [200, 531],
    'clear': [800, 800]
}

TEMPERATURE_ID ={
    'dubak': [-35, 5],
    'prohladno': [5, 15],
    'zaebok': [15, 20],
    'szara': [20, 35],
}

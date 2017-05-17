
STYLE_LIST = (
('C', 'casual'),
('B', 'bussines'),
('S', 'sport'),
('P', 'party'),
)

ITEM_TYPE_LIST =(
('', 'type'),
('dress', 'dress'),
('blouse', 'blouse'),
('pants', 'pants'),
('footwear', 'footwear'),
('outerwear', 'outerwear'),
('umbrella', 'umbrella'),
('glasses', 'glasses'),
('bag', 'bag'),
('skirt', 'skirt'),
('cap', 'cap'),
('tshirt', 'Tshirt'),
('sneakers', 'Sneakers'),
('shoes', 'Shoes'),
('boots', 'Boots'),
)

#справочная инфа для фронта
body = ('dress', 'blouse', 'tshirt')
pants = ('pants', 'skirt')
outerwear = ('outerwear',)
glasses = ('cap', 'glasses')
shoes = ('sneakers', 'shoes', 'boots', 'footwear')
bag = ('bag',)

TYPES_OF_ITEMS = {
        'body': ('dress', 'blouse', 'tshirt'),
        'pants': ('pants', 'skirt'),
        'shoes': ('sneakers', 'shoes', 'boots', 'footwear'),
        'outerwear' : ('outerwear'),
        'accessory':('cap', 'glasses', 'bag')
    }

COLOR_LIST = (
('black', 'black'),
('white','white'),
('milk','milk'),
('beige','beige'),
('deep_blue','deep_blue'),
('olivaceous','olivaceous'),
('deep_green','deep_green'),
('vinous','vinous'),
('chocolate','chocolate'),
('blue','blue'),
('pink','pink'),
('coral','coral'),
('red','red'),
('yellow','yellow'),
('purple','purple'),
('gray','gray'),
)

SEASON_LIST = (
('Wn', 'winter'),
('Sp', 'spring'),
('Sm', 'summer'),
('At', 'autumn'),
('SS', 'spring-summer'),
('AW', 'autumn-winter'),
)

TEMPERATURE_LIST =(
('all', 'all'),
('dubak', "-35_+5"),
('prohladno', "+5_+15"),
('zaebok', "+15_+20"),
('szara', "+20_+35"),
)

SKY_LIST = (
('clouds', 'Clouds'),
('rain', 'Rain'),
('clear', 'Clear'),
)

SEX_LIST = (
('M', 'male'),
('F', 'female')
)

LIST_OF_TYPES = ['body', 'pants', 'shoes', 'outerwear', 'accessory']

KOLOR_DIKT = {
        'black': 'all',
        'white': 'all',
        'beige': 'all',
        'olive': 'white_beige_blue_blue',
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

seasons = {
        'Wn': [12, 1, 2],
        'Sp': [3, 4 ,5],
        'Sm': [6, 7, 8],
        'At': [9, 10, 11],
        'SS': [3, 4, 5, 6, 7, 8],
        'AW': [9, 10, 11, 12, 1, 2],
}


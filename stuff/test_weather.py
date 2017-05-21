
import unittest, json
from weather import Weather


class TestWether(unittest.TestCase):
    city_id = 524894
    city_id_false = 1
    dict = Weather().weather_dictionary(city_id)
    print(Weather().data_output(city_id))
    def test_weather_dict(self):
        dict = self.dict
        if dict['city'] == 'Moskva':
            print(dict)
            return True
        else:
            raise BaseException('Город с таким id не найден')

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestWether)
unittest.TextTestRunner().run(suite)
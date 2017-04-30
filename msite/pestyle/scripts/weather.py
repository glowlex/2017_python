import datetime
import json
import urllib.request

class Weather():
    def __time_converter(self, time):
        converted_time = datetime.datetime.fromtimestamp(int(time)).strftime('%I:%M %p')
        return converted_time

    def __url_builder(self, city_id):
        with open('./pestyle/scripts/config.json') as file_config:
            config = json.load(file_config)
        user_api = config['user_api']
        unit = 'metric'
        api = 'http://api.openweathermap.org/data/2.5/weather?id='
        full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api

        return full_api_url

    def __data_fetch(self, full_api_url):
        url = urllib.request.urlopen(full_api_url)
        output = url.read().decode('utf-8')
        raw_api_dict = json.loads(output)
        url.close()

        return raw_api_dict

    def weather_dictionary(self, city_id):
        raw_api_dict = self.__data_fetch(self.__url_builder(city_id))

        return dict(
            city=raw_api_dict.get('name'),
            country=raw_api_dict.get('sys').get('country'),
            temp=raw_api_dict.get('main').get('temp'),
            temp_max=raw_api_dict.get('main').get('temp_max'),
            temp_min=raw_api_dict.get('main').get('temp_min'),
            humidity=raw_api_dict.get('main').get('humidity'),
            pressure=raw_api_dict.get('main').get('pressure'),
            sky=raw_api_dict['weather'][0]['main'],
            sunrise=self.__time_converter(raw_api_dict.get('sys').get('sunrise')),
            sunset=self.__time_converter(raw_api_dict.get('sys').get('sunset')),
            wind=raw_api_dict.get('wind').get('speed'),
            wind_deg=raw_api_dict.get('deg'),
            dt=self.__time_converter(raw_api_dict.get('dt')),
            cloudiness=raw_api_dict.get('clouds').get('all')
        )
# def data_output(city_id):
#     data = Weather().weather_dictionary(city_id)
#
#     m_symbol = '\xb0' + 'C'
#     print('---------------------------------------')
#     print('Current weather in: {}, {}:'.format(data['city'], data['country']))
#     print(data['temp'], m_symbol, data['sky'])
#     print('Max: {}, Min: {}'.format(data['temp_max'], data['temp_min']))
#     print('')
#     print('Wind Speed: {}, Degree: {}'.format(data['wind'], data['wind_deg']))
#     print('Humidity: {}'.format(data['humidity']))
#     print('Cloud: {}'.format(data['cloudiness']))
#     print('Pressure: {}'.format(data['pressure']))
#     print('Sunrise at: {}'.format(data['sunrise']))
#     print('Sunset at: {}'.format(data['sunset']))
#     print('')
#     print('Last update from the server: {}'.format(data['dt']))
#     print('---------------------------------------')


# moscow_id = 524901

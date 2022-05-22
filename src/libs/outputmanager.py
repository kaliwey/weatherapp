
from libs.apiweather import Apiweather

class OutputManager(Apiweather):

    def __init__(self, apiweather):
        self.city = apiweather.city.upper()
        self.country_code = apiweather.country_code
        self.units = apiweather.units

    def printOutput(self, data):
        try:
            print(data)
            print(self.units)
            print(f'{self.city} ({self.country_code})')
            print(f'> Weather: {data["weather"][0]["description"]}')
            print(f'> Temperature: {data["main"]["temp"]} ºC')
        except Exception as e:
            print(e)

from operator import length_hint
from libs.apiweather import Apiweather
from libs.dataenums import Units
import datetime
import logging

logger = logging.getLogger(__name__)

class OutputManagerMeta(type):
    """
    Metaclass for limit instances to one
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
class OutputManager(Apiweather,metaclass=OutputManagerMeta):

    def __init__(self, apiweather):
        self.city = apiweather.city.upper()
        self.country_code = apiweather.country_code
        self.units = apiweather.units
        self.days = apiweather.days

    @staticmethod
    def printDate():
        today = datetime.date.today()
        return today.strftime('%b %d, %Y')

    @staticmethod
    def parseTimeStampToDate(ts):
        dt = datetime.datetime.fromtimestamp(ts)
        return dt.strftime('%b %d, %Y')

    def printUnitSymbol(self):
        if self.units == Units.metric.name:
            return "ºC"
        if self.units == Units.imperial.name:
            return "ºF"
    
    def printOutputCurrentWeather(self, data):
        try:
            print(self.printDate())
            print(f'{self.city} ({self.country_code})')
            print(f'> Weather: {data["weather"][0]["description"]}')
            print(f'> Temperature: {data["main"]["temp"]} {self.printUnitSymbol()}')
        except Exception as e:
            print(e)
    
    def printOutputForecast(self, data):
        try:
            data = data["daily"]
            # Removing last n days to match max days selected by user
            days_to_remove = len(data) - self.days
            del data[-days_to_remove:]

            print(f'{self.city} ({self.country_code})')
            for i in data:
                print(self.parseTimeStampToDate(i['dt']))
                print(f'> Weather: {i["weather"][0]["main"]}')
                print(f'> Temperature: {i["temp"]["day"]} {self.printUnitSymbol()}')

        except Exception as e:
            print(e)
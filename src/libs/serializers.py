from libs.enumsfile import Units, Mode
import logging
from config.config import config
import datetime

logger = logging.getLogger(__name__)


class Serializer():
    def __init__(self, initial_setup, arg):
        self.datainput = arg
        self.city = initial_setup.city
        self.country_code = initial_setup.country_code
        self.units = initial_setup.units

    @staticmethod
    def print_date():
        today = datetime.date.today()
        return today.strftime('%b %d, %Y')

    @staticmethod
    def parse_time_stamp_to_date(ts):
        dt = datetime.datetime.fromtimestamp(ts)
        return dt.strftime('%b %d, %Y')

    def print_unit_symbol(self):
        if self.units == Units.imperial.name:
            return "ºF"
        else:
            return "ºC"


class SerializerCurrentWeather(Serializer):
    def __init__(self, initial_setup, arg):
        super().__init__(initial_setup, arg)

    def print_output(self):
        try:
            output = f'\n{self.print_date()}\n'
            output += f'{self.city.upper()} ({self.country_code})\n'
            output += f'> Weather: {self.datainput["weather"][0]["description"]}\n'
            output += f'> Temperature: {self.datainput["main"]["temp"]} {self.print_unit_symbol()}\n'
            print(output)
        except Exception as e:
            logging.error(e)
 


class SerializerForecastWeather(Serializer):
    def __init__(self, initial_setup, arg):
        super().__init__(initial_setup, arg)
        self.days = initial_setup.days

    def print_output(self):
        try:
            data = self.datainput["daily"]
            # Removing last n days to match max days selected by user
            if len(data) > self.days:
                days_to_remove = len(data) - self.days
                del data[-days_to_remove:]

            output = f'\n{self.city.upper()} ({self.country_code})\n'
            for i in data:
                output += f'{self.parse_time_stamp_to_date(i["dt"])}\n'
                output += f'> Weather: {i["weather"][0]["main"]}\n'
                output += f'> Temperature: {i["temp"]["day"]} {self.print_unit_symbol()}\n'
            print(output)

        except Exception as e:
            logging.error(e)
 


class AbstractSerializerFactory:
    def create_serializer(self, initial_setup, arg):
        pass
 
class SerializerFactory(AbstractSerializerFactory):
    def create_serializer(self, initial_setup, arg):
        Serializer = None
        if initial_setup.mode == Mode.current.name:
            return SerializerCurrentWeather(initial_setup, arg)
        elif initial_setup.mode == Mode.forecast.name:
            return SerializerForecastWeather(initial_setup, arg)
        else:
            return

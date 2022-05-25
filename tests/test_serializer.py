import pytest
import os
import sys
import datetime

current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current)
parent = os.path.dirname(current) + "/src"
sys.path.append(parent)

from libs.apifactory import ApiFactory
from libs.serializers import SerializerFactory

current = {
    "city": "Madrid",
    "country_code": "ES",
    "units": "metric",
    "mode": "current"
}
forecast = {
    "city": "Madrid",
    "country_code": "ES",
    "units": "metric",
    "mode": "forecast",
    "days": 3
}

current_data = {}
forecast_data = {}

class InitialSetup():
    def __init__(self, arg):
        self.city = arg["city"]
        self.country_code = arg["country_code"]
        self.units = arg["units"]
        self.days = arg["days"] if "days" in arg else None
        self.mode = arg["mode"]
        self.apikey = ""
        self.headers = ""
        self.api_weather_url = ""


factory_serializer = SerializerFactory()
current_initial_setup = InitialSetup(current)
forecast_initial_setup = InitialSetup(forecast)


@pytest.fixture
def serializer_current_weather():
    '''Returns a Serializer instance for current weather'''
    return factory_serializer.create_serializer(current_initial_setup, current_data)

@pytest.fixture
def serializer_forecast_weather():
    '''Returns a Serializer instance for current weather'''
    return factory_serializer.create_serializer(forecast_initial_setup, forecast_data)




'''Test parse_time_stamp_to_date'''
@pytest.mark.parametrize("ts", [
    (1653384586),
    (165338),
    (0)
    ])
def test_serializer_time_stamp_to_date(serializer_current_weather, ts):
    dt = datetime.datetime.fromtimestamp(ts)
    assert serializer_current_weather.parse_time_stamp_to_date(ts) == dt.strftime('%b %d, %Y')


'''Test print_date'''
def test_serializer_print_date(serializer_current_weather):
    now = datetime.datetime.now()
    assert serializer_current_weather.print_date() == now.strftime('%b %d, %Y')


'''Test print_units_symbol'''
@pytest.mark.parametrize("units", [
    ("metric"),
    ("imperial"),
    (""),
    (None),
    ("random")
    ])
def test_serializer_print_units_symbol(serializer_current_weather, units):
    serializer_current_weather.units = units
    if serializer_current_weather.units == 'imperial':
        assert serializer_current_weather.print_unit_symbol() == "ºF"
    else:
        assert serializer_current_weather.print_unit_symbol() == "ºC"

'''Test print_output_current_weather'''
@pytest.mark.parametrize("city,country_code,units,data", [
    ("Madrid","ES","metric",{
        "weather":[{"description":"clear"}],
        "main":{"temp":25.4}
        }),
    ("Madrid","ES","imperial",{
        "weather":[{"description":"clear"}],
        "main":{"temp":-10.4}
        }),
    ("Madrid","ES","",{
        "weather":[{"description":"clear"}],
        "main":{"temp":25.4}
        }),
    ("Madrid","ES",None,{
        "weather":[{"description":"clear"}],
        "main":{"temp":None}
        }),
    ("Madrid","ES","decimal",{
        "weather":[{"description":"clear"}],
        "main":{"temp":""}
        })
    ])
def test_print_output_current_weather(serializer_current_weather, city, country_code, units, data, capfd):
    serializer_current_weather.units = units
    serializer_current_weather.city = city
    serializer_current_weather.country_code = country_code
    serializer_current_weather.datainput = data
    serializer_current_weather.print_output()

    today = datetime.date.today().strftime('%b %d, %Y')
    weather = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    symbol = serializer_current_weather.print_unit_symbol()

    out, err = capfd.readouterr()
    output =  f'\n{today}\n'
    output += f'{city.upper()} ({country_code})\n'
    output += f'> Weather: {weather}\n'
    output += f'> Temperature: {temperature} {symbol}\n\n'
    assert out == output


'''Test print_output_forecast_weather'''
@pytest.mark.parametrize("city,country_code,units,days,data", [
    ("Madrid","ES","metric",1,{'daily': [{
            'dt': 1653393600,
            'temp': {'day': 22.45}, 
            'weather': [{
                'main': 'Rain'
                }]
            },
            {
            'dt': 1653393600,
            'temp': {'day': 22.45}, 
            'weather': [{
                'main': 'Rain', 
                }]
            }]
        })
    ])
def test_print_output_forecast_weather(serializer_forecast_weather, city, country_code, units, days, data, capfd):
    serializer_forecast_weather.units = units
    serializer_forecast_weather.city = city
    serializer_forecast_weather.country_code = country_code
    serializer_forecast_weather.days = days
    serializer_forecast_weather.datainput = data
    serializer_forecast_weather.print_output()

    data = data["daily"]
    if len(data) > serializer_forecast_weather.days:
        days_to_remove = len(data) - serializer_forecast_weather.days
        del data[-days_to_remove:]

    symbol = serializer_forecast_weather.print_unit_symbol()
    out, err = capfd.readouterr()

    output = f'\n{city.upper()} ({country_code})\n'
    for i in data:
        date = serializer_forecast_weather.parse_time_stamp_to_date(i['dt'])
        output += f'{date}\n'
        output += f'> Weather: {i["weather"][0]["main"]}\n'
        output += f'> Temperature: {i["temp"]["day"]} {symbol}\n\n'
    assert out == output
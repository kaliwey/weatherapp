import pytest
import os
import sys
import datetime

current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current)
parent = os.path.dirname(current) + "/src"
sys.path.append(parent)

from libs.outputmanager import OutputManager
from libs.apiweather import Apiweather

city = "Madrid"
country_code = "ES"
units = "metric"
days = 2


@pytest.fixture
def no_units_apiweather():
    '''Returns an Apiweather instance without units'''
    return Apiweather(city,country_code,days)

@pytest.fixture
def api_weather():
    '''Returns a Apiweather instance with all attributes'''
    return Apiweather(city,country_code,units,days)





'''Test parse_time_stamp_to_date'''
@pytest.mark.parametrize("ts", [
    (1653384586),
    (165338),
    (0)
    ])
def test_parse_time_stamp_to_date(api_weather, ts):
    outputmanager = OutputManager(api_weather)
    dt = datetime.datetime.fromtimestamp(ts)
    assert outputmanager.parse_time_stamp_to_date(ts) == dt.strftime('%b %d, %Y')


'''Test outputmanager_print_dat'''
def test_outputmanager_print_date(api_weather):
    outputmanager = OutputManager(api_weather)
    now = datetime.datetime.now()
    assert outputmanager.print_date() == now.strftime('%b %d, %Y')


'''Test print_units_symbol'''
@pytest.mark.parametrize("units", [
    ("metric"),
    ("imperial"),
    (""),
    (None),
    ("random")
    ])
def test_print_units_symbol(no_units_apiweather, units):
    outputmanager = OutputManager(no_units_apiweather)
    outputmanager.units == units
    if outputmanager.units == "imperial":
        assert outputmanager.print_unit_symbol() == "ºF"
    else:
        assert outputmanager.print_unit_symbol() == "ºC"


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
def test_print_output_current_weather(api_weather, city, country_code, units, data, capfd):
    outputmanager = OutputManager(api_weather)
    outputmanager.units == units
    outputmanager.city == city
    outputmanager.country_code == country_code
    outputmanager.print_output_current_weather(data)
    weather = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    symbol = outputmanager.print_unit_symbol()
    out, err = capfd.readouterr()
    assert out == f"May 24, 2022\n{city.upper()} ({country_code})\n> Weather: {weather}\n> Temperature: {temperature} {symbol}\n"


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
def test_print_output_forecast_weather(api_weather, city, country_code, units, days, data, capfd):
    outputmanager = OutputManager(api_weather)
    outputmanager.units == units
    outputmanager.city == city
    outputmanager.country_code == country_code
    outputmanager.days == days
    outputmanager.print_output_forecast(data)
    data = data["daily"]
    if len(data) > outputmanager.days:
        days_to_remove = len(data) - outputmanager.days
        del data[-days_to_remove:]
    symbol = outputmanager.print_unit_symbol()
    out, err = capfd.readouterr()

    output = f'{city.upper()} ({country_code})\n'
    for i in data:
        date = outputmanager.parse_time_stamp_to_date(i['dt'])
        output += f'{date}\n'
        output += f'> Weather: {i["weather"][0]["main"]}\n> Temperature: {i["temp"]["day"]} {symbol}\n'
    assert out == output

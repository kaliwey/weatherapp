import requests
import os
from enum import Enum
import json
import functools
import sys
from config.config import config


class Units(Enum):
    imperial = 1
    metric   = 2

    @classmethod
    def default(enumcls):
        return enumcls.METRIC


class Apiweather(object):
    """
    The Subsystem can accept requests either from the facade or client directly.
    In any case, to the Subsystem, the Facade is yet another client, and it's
    not a part of the Subsystem.
    """
    def __init__(self, city, country_code, units):
        self.city = city
        self.country_code = country_code
        self.units = units or Units.default()
        self.__geocoding_url = str(config.get('base_urls','apigeocoding'))
        self.__weather_url = str(config.get('base_urls','apiweather'))
        self.__apikey = os.getenv('APIKEY')
        self.__current_weather_ep = str(config.get('endpoints','current_weather'))
        self.__forecast_weather_ep = str(config.get('endpoints','forecast_weather'))
        self.headers = {
            'Content-Type': 'application/json',
            }


    def _request(self, params, url, endpoint=""):
        return requests.get(f'{url}{endpoint}', params=params, headers=self.headers)


    def geocoder(func):
        print("hola")
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            params = {
                'q': self.city + "," + self.country_code,
                'limit': 5,
                'appid': str(self.__apikey)
            }
            r = self._request(params, self.__geocoding_url)
            # r = requests.get(f'{self.geocoding_url}', params=params, headers=self.headers)
            if 200 <= r.status_code <= 299:
                r = r.json()
                self.__lat = r[0]["lat"] if "lat" in r[0] else None
                self.__lon = r[0]["lon"] if "lon" in r[0] else None
            else:
                print(r.status_code)
            return func(self, *args, **kwargs)
        return wrap

    
    @geocoder
    def getCurrentWeather(self):
        try:
            if (self.__lat is not None) and (self.__lon is not None):
                params = {
                    'lat': self.__lat,
                    'lon': self.__lon,
                    'units': "metric",
                    'appid': str(self.__apikey)
                }
            else:
                params = {
                    'city name': self.city,
                    'country code': self.country_code,
                    'units': "metric",
                    'appid': str(self.__apikey)
                }
            
                
            r = self._request(params, self.__weather_url, self.__current_weather_ep)
            
            if 200 <= r.status_code <= 299:
                r = r.json()
                return r
            #         return nmkutils.LoginCodes.LOGIN_ERR_BAD_CREDENTIALS.value
            # else:
            #     # self._network_status.set_connection_status(nmkutils.StatusCodes.IS_KO)
            #     return nmkutils.LoginCodes.LOGIN_ERR_BAD_JSON_FORMAT.value
        except Exception as e:
            # logging.info("Exception on login:", e)
            pass
            # return nmkutils.ApiCodes.APICALL_ERR_NOK.value

    def getForecast(self):
        return "t"

    def operation1(self) -> str:
        return "Subsystem1: Ready!"

    # ...

    def operation_n(self) -> str:
        return "Subsystem1: Go!"
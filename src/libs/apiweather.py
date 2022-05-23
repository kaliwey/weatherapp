import os
import sys
import requests
import functools
from config.config import config
from libs.dataenums import Units
import logging

logger = logging.getLogger(__name__)

class Apiweather(object):
    """
    Class for connect with Api Weather services
    """
    def __init__(self, city, country_code, units, days):
        self.city = city
        self.country_code = country_code
        self.units = units or Units.default()
        self.days = days
        self.__geocoding_url = str(config.get('base_urls','apigeocoding'))
        self.__weather_url = str(config.get('base_urls','apiweather'))
        self.__apikey = os.getenv('APIKEY')
        self.__current_weather_ep = str(config.get('endpoints','current_weather'))
        self.__forecast_weather_ep = str(config.get('endpoints','forecast_weather'))
        self.headers = {
            'Content-Type': 'application/json',
            }


    def _request(self, params, url, endpoint=""):
        try:
            r = requests.get(f'{url}{endpoint}', params=params, headers=self.headers)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as e:
            logging.info(e.response.text)


    def geocoder(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            params = {
                'q': self.city + "," + self.country_code,
                'limit': 5,
                'appid': str(self.__apikey)
            }
            r = self._request(params, self.__geocoding_url)

            try:
                if hasattr(r, "status_code"):
                    if 200 <= r.status_code <= 299:
                        r = r.json()
                        self.__lat = r[0]["lat"] if "lat" in r[0] else None
                        self.__lon = r[0]["lon"] if "lon" in r[0] else None
                    else:
                        print(r.status_code)
                else:
                    sys.exit()
            except Exception as e:
                logging.info(e)
            return func(self, *args, **kwargs)
        return wrap

    
    @geocoder
    def get_current_weather(self):
        try:
            logging.debug("getting current weather")
            if (self.__lat is not None) and (self.__lon is not None):
                params = {
                    'lat': self.__lat,
                    'lon': self.__lon,
                    'units': self.units,
                    'appid': str(self.__apikey)
                }
            else:
                params = {
                    'city name': self.city,
                    'country code': self.country_code,
                    'units': self.units,
                    'appid': str(self.__apikey)
                }
            
                
            r = self._request(params, self.__weather_url, self.__current_weather_ep)
            if hasattr(r, "status_code"):
                if 200 <= r.status_code <= 299:
                    r = r.json()
                    return r
                else:
                    print(f'Error: {r.status_code}')
                    sys.exit()
            else:
                sys.exit()
        except Exception as e:
            logging.info(e)

    @geocoder
    def get_forecast(self):
        try:
            logging.debug("getting forecast weather")
            if (self.__lat is not None) and (self.__lon is not None):
                params = {
                    'lat': self.__lat,
                    'lon': self.__lon,
                    'units': self.units,
                    'exclude': "current,minutely,hourly,alerts",
                    'appid': str(self.__apikey)
                }
            else:
                params = {
                    'city name': self.city,
                    'country code': self.country_code,
                    'units': self.units,
                    'exclude': "current,minutely,hourly,alerts",
                    'appid': str(self.__apikey)
                }
            
                
            r = self._request(params, self.__weather_url, self.__forecast_weather_ep)

            if hasattr(r, "status_code"):
                if 200 <= r.status_code <= 299:
                    r = r.json()
                    return r
                else:
                    print(f'Error: {r.status_code}')
                    sys.exit()
            else:
                sys.exit()
        except Exception as e:
            logging.info(e)
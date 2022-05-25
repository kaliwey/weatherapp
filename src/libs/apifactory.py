from libs.enumsfile import Units, Mode
import requests
import logging
import sys
from config.config import config
import functools

logger = logging.getLogger(__name__)


class Api():
    def __init__(self, arg):
        self.city = arg.city
        self.country_code = arg.country_code
        self.units = arg.units or Units.default()
        self.apikey = arg.apikey
        self.headers = arg.headers
        self.api_weather_url = arg.api_weather_url

    def _request(self, params, url, endpoint=""):
        try:
            r = requests.get(f'{url}{endpoint}', params=params, headers=self.headers)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as e:
            logging.error(e.response.text)

    def _check_response(self, response):
        if hasattr(response, "status_code"):
            if 200 <= response.status_code <= 299:
                return True
            else:
                logging.info(f'Error: {response.status_code}')
                return False
        else:
            logging.info(f'Bad response')
            return False
    
    @staticmethod
    def geocoder(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            params = {
                'q': self.city + "," + self.country_code,
                'limit': 5,
                'appid': str(self.apikey)
            }
            r = self._request(params, str(config.get('base_urls','apigeocoding')))

            try:
                if hasattr(r, "status_code"):
                    if 200 <= r.status_code <= 299:
                        r = r.json()
                        self.lat = r[0]["lat"] if "lat" in r[0] else None
                        self.lon = r[0]["lon"] if "lon" in r[0] else None
                    else:
                        logging.info(r.status_code)
                else:
                    sys.exit()
            except Exception as e:
                logging.error(e)
            return func(self, *args, **kwargs)
        return wrap


class CurrentWeather(Api):
    def __init__(self, arg):
        super().__init__(arg)
        self.__current_weather_ep = str(config.get('endpoints','current_weather'))

    @Api.geocoder
    def _set_params(self):
        if (self.lat is not None) and (self.lon is not None):
            params = {
                'lat': self.lat,
                'lon': self.lon,
                'units': self.units,
                'appid': str(self.apikey)
            }
        else:
            params = {
                'city name': self.city,
                'country code': self.country_code,
                'units': self.units,
                'appid': str(self.apikey)
            }
        return params

    def get_data(self):
        try:
            logging.debug("getting current weather")
            params = self._set_params() 
            r = self._request(params, self.api_weather_url, self.__current_weather_ep)
            return r.json() if self._check_response(r) else sys.exit()
        except Exception as e:
            logging.error(e)


class ForecastWeather(Api):
    def __init__(self, arg):
        super().__init__(arg)
        self.days = arg.days
        self.__forecast_weather_ep = str(config.get('endpoints','forecast_weather'))

    @Api.geocoder
    def _set_params(self):
        if hasattr(self, "lat") and hasattr(self, "lon"):
            if (self.lat is not None) and (self.lon is not None):
                params = {
                    'lat': self.lat,
                    'lon': self.lon,
                    'units': self.units,
                    'exclude': "current,minutely,hourly,alerts",
                    'appid': str(self.apikey)
                }
        else:
            logging.info("No latitud and longitud params, exiting")
            sys.exit()
        return params

    def get_data(self):
        try:
            logging.debug("getting current weather")
            params = self._set_params() 
            r = self._request(params, self.api_weather_url, self.__forecast_weather_ep)
            return r.json() if self._check_response(r) else sys.exit()
        except Exception as e:
            logging.error(e)
 
 
class AbstractApiFactory:
    def create_api(self, arg):
        pass
 
class ApiFactory(AbstractApiFactory):
    def create_api(self, arg):
        Api = None
        if arg.mode == Mode.current.name:
            return CurrentWeather(arg)
        elif arg.mode == Mode.forecast.name:
            return ForecastWeather(arg)
        else:
            return

import os
import sys
from libs.enumsfile import Units
from config.config import config
class BootSetup():
    def __init__(self, args):
        self.checkApiKey()
        self.city = args.city
        self.country_code = args.country_code
        self.units = args.units or Units.default()
        self.days = args.days if args.days else None
        self.mode = args.mode
        self.apikey = os.getenv('APIKEY')
        self.headers = {
            'Content-Type': 'application/json',
            }
        self.api_weather_url = str(config.get('base_urls','apiweather'))

    def checkApiKey(self):
        if len(os.getenv('APIKEY')) == 0:
            print("Please, fill APIKEY value in .env file")
            sys.exit()
        elif len(os.getenv('APIKEY')) < 32:
            print("APIKEY length no valid, please check it")
            sys.exit()
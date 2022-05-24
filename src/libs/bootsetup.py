import os
import sys

class BootSetup():
    
    def checkApiKey(self):
        if len(os.getenv('APIKEY')) == 0:
            print("Please, fill APIKEY value in .env file")
            sys.exit()
        elif len(os.getenv('APIKEY')) < 32:
            print("APIKEY length no valid, please check it")
            sys.exit()
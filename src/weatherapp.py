#!/usr/bin/env python3

from libs.cli import Cli
from libs.apiweather import Apiweather
from libs.outputmanager import OutputManager
from libs.dataenums import Mode
import sys
import logging
from config import loggingconfig


if __name__ == "__main__":

    console = Cli()

    logging.debug(sys.argv)
    logging.debug(console.config)

    try:
        if (console.city) and (console.country_code):
            apiweather = Apiweather(console.city, console.country_code, console.units, console.days)
            printer = OutputManager(apiweather)

            if console.mode == Mode.current.name:
                printer.printOutputCurrentWeather(apiweather.getCurrentWeather())

            if console.mode == Mode.forecast.name:
                printer.printOutputForecast(apiweather.getForecast())
        else:
            print("No city or Country Code, please fill them")
            sys.exit()
    except Exception as e:
        logging.info(e)       
    

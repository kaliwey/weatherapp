#!/usr/bin/env python3

from libs.cli import Cli
from libs.enumsfile import Mode
from libs.bootsetup import BootSetup
from libs.apifactory import ApiFactory
from libs.serializers import SerializerFactory
import sys
import logging
from config import loggingconfig


if __name__ == "__main__":

    console = Cli()

    # This object has all console inputs and config data needed for APIs and Serializers
    initial_setup = BootSetup(console)

    try:
        if (initial_setup.city) and (initial_setup.country_code):
            factory_api = ApiFactory()
            factory_serializer = SerializerFactory()
            
            # for current weather
            if initial_setup.mode == Mode.current.name:
                api_current = factory_api.create_api(initial_setup)
                serializer_current = factory_serializer.create_serializer(initial_setup, api_current.get_data())
                serializer_current.print_output()

            # for forecast
            if initial_setup.mode == Mode.forecast.name:
                api_forecast = factory_api.create_api(initial_setup)
                serializer_forecast = factory_serializer.create_serializer(initial_setup, api_forecast.get_data())
                serializer_forecast.print_output()

        else:
            logging.info("No city or Country Code, please fill them")
            sys.exit()

    except Exception as e:
        logging.error(e)       
    

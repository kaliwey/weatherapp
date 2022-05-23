from libs.cli import Cli
from libs.apiweather import Apiweather
from libs.outputmanager import OutputManager
from libs.dataenums import Mode
import sys


if __name__ == "__main__":


    print(sys.argv)
    console = Cli()
    print(console.config)

    try:
        if (console.city) and (console.country_code):
            apiweather = Apiweather(console.city, console.country_code, console.units, console.days)
            adapter = OutputManager(apiweather)

            if console.mode == Mode.current.name:
                adapter.printOutputCurrentWeather(apiweather.getCurrentWeather())

            if console.mode == Mode.forecast.name:
                adapter.printOutputForecast(apiweather.getForecast())
        else:
            print("No city or Country Code, please fill them")
    except Exception as e:
        print(e)       
    

from libs.cli import Cli
from libs.apiweather import Apiweather
from libs.outputmanager import OutputManager
import sys



def client_code(target: "apiweather.Apiweather") -> None:
    """
    The client code supports all classes that follow the Target interface.
    """
    print("entra")
    target.getCurrentWeather()

if __name__ == "__main__":

    # The client code may have some of the subsystem's objects already created.
    # In this case, it might be worthwhile to initialize the Facade with these
    # objects instead of letting the Facade create new instances.


    print(sys.argv)
    console = Cli()
    print(console.config)
    print(console.units)
    print(console.city)
    print(console.country_code)

    try:
        if (console.city) and (console.country_code):
            apiweather = Apiweather(console.city, console.country_code, console.units)
            adapter = OutputManager(apiweather)

            adapter.printOutput(apiweather.getCurrentWeather())
    except:
        pass       
    

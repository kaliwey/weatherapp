from argparse import ArgumentParser, Action, ArgumentError
import sys
from libs.dataenums import Mode

class CliMeta(type):
    """
    Metaclass for limit instances to one
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class SplitSpacesAction(Action):
    """
    Class for split spaces on argument City,CC when city name has spaces
    """
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            setattr(namespace, self.dest, ' '.join(values))
        except:
            raise ArgumentError("%s is not a valid argument" % values)

class Cli(metaclass=CliMeta):
    """
    Class for command line interface
    """
    def __init__(self):
        self.parser = ArgumentParser(description=__doc__)

        self.parser.add_argument(
            "mode", 
            help="Current or Forecast wheather", 
            choices=['current', 'forecast']
        )

        self.parser.add_argument(
            "location",
            help='a comma separated values as City,Country-Code, i.e Madrid,ES',
            nargs='+',
            action=SplitSpacesAction
        )

        self.parser.add_argument(
            "--units",
            help="Units to show the result",
            default="metric",
            choices=['imperial', 'metric']
        )

        self.parser.add_argument(
            "--days",
            type=int,
            choices=range(1,9),
            required=Mode.forecast.name in sys.argv,
            help="Number of days to forecast wheather",
        )

        self.config = vars(self.parser.parse_args(namespace=self))

        self.mode = self.config["mode"]
        self.city = self.config["location"].split(",")[0]
        self.country_code = self.config["location"].split(",")[1]
        self.units = self.config["units"]
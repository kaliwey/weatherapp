from argparse import ArgumentParser, Action, ArgumentError

# class SplitArgs(Action):
#     def __call__(self, parser, namespace, values, option_string=None):
#         # Be sure to strip, maybe they have spaces where they don't belong and wrapped the arg value in quotes
#         setattr(namespace, self.dest, [value.strip() for value in values.split(",")])

# class StripArgument(Action):
#     def __call__(self, parser, namespace, values, option_string=None):
#         setattr(namespace, self.dest, values.strip())

class SplitSpacesAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            setattr(namespace, self.dest, ' '.join(values))
        except:
            raise ArgumentError("%s is not a valid argument" % values)

# class DelimiterSeperatedInput:
#     def __init__(self, item_type, separator=',', separator2=' '):
#         self.item_type = item_type
#         self.separator = separator
#         self.separator2 = separator2

#     def __call__(self, value):
#         print(value)
#         values = []
#         try:
#             if not self.separator in value:
#                 raise ArgumentError("%s is not a valid argument" % value)

#             for val in value.split(self.separator):
#                 typed_value = self.item_type(val)
#                 values.append(typed_value)
#         except Exception:
#             raise ArgumentError("%s is not a valid argument" % value)
#         return values

class Cli:
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
            help="skip files that exist",
            default="metric",
            choices=['imperial', 'metric']
        )

        self.args = self.parser.parse_args(namespace=self)
        self.config = vars(self.args)

        self.city = self.config["location"].split(",")[0]
        self.country_code = self.config["location"].split(",")[1]
        self.units = self.config["units"]


# parser = ArgumentParser(description="Just an example", formatter_class=ArgumentDefaultsHelpFormatter)
# # parser.add_argument("-c", "--country", default="SE", help="Two-letter country code")
# # parser.add_argument("-a", "--archive", action="store_true", help="archive mode")
# # parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
# # parser.add_argument("-B", "--block-size", help="checksum blocksize")
# parser.add_argument("--units", help="skip files that exist", default="imperial", choices=['imperial', 'metric'])
# # parser.add_argument("--exclude", help="files to exclude")
# parser.add_argument("type", help="Source location", choices=['current', 'forecast'])
# parser.add_argument("city", help="City location")
# parser.add_argument("country code", help="Country Code, ie. ES, US, UK")

# args = parser.parse_args()
# config = vars(args)

# print(config)
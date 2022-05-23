try:
    import configparser
except:
    from six.moves import configparser

class CaseConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

config = CaseConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read_file(open('src/config/config.ini'))
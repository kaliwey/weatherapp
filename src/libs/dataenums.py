from enum import Enum

class Units(Enum):
    imperial = 1
    metric   = 2

    @classmethod
    def default(enumcls):
        return enumcls.metric

class Mode(Enum):
    current  = 1
    forecast = 2
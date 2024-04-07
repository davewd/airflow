__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"

from enum import Enum


class ConfigurationFileTypeEnum(Enum):
    DEFAULTS = 1
    TASK = 2
    PARALLEL_TASK = 3
    PARALLEL_TASK_GENERATOR = 4
    UNKNOWN = 5

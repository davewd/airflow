__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"
from lib.market_data.ecb.fx_api import get_ecb_data_api
import datetime


def main(args):
    data = get_ecb_data_api(start_date=datetime.date(2024, 3, 22), end_date=datetime.date(2024, 3, 31))
    print(data)


if __name__ == "__main__":
    main()

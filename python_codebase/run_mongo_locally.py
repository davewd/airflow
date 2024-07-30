__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"

import dwdrun.dynamic_import_lib
import logging

logger = logging.getLogger(__name__)

# Example usage:
if __name__ == "__main__":
    try:
        from lib.market_data.ecb import fx_api
        import datetime

        data = fx_api.get_ecb_data_api(start_date=datetime.date(2024, 3, 22), end_date=datetime.date(2024, 3, 31))
        logger.info(data)
        print(f"{data}")
        # You can now use the module as usual
    except ImportError as e:
        print(e)

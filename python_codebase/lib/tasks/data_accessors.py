__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"
import asana
from asana.rest import ApiException
from pprint import pprint


# Set up your Asana Personal Access Token
personal_access_token = "2/32071810162863/1207022667128530:a29ef15ca2078366b90696cc10d91c68"


configuration = asana.Configuration()
configuration.access_token = "<YOUR_ACCESS_TOKEN>"
api_client = asana.ApiClient(configuration)

# create an instance of the API class
users_api_instance = asana.UsersApi(api_client)
user_gid = "mi_capital"
opts = {}

try:
    # Get a user
    user = users_api_instance.get_user(user_gid, opts)
    pprint(user)
except ApiException as e:
    print("Exception when calling UsersApi->get_user: %s\n" % e)

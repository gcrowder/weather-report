import requests

from weather_lib import Location, Hurricane, Conditions, Forecast, Astronomy

from secrets import SECRET_TOKEN
zip_code = 92651
features = ['astronomy', 'forecast', 'geolookup', 'conditions', 'currenthurricane', 'alerts']
feature_string = "{}/{}/{}/{}/{}/{}".format(*features)
url = 'http://api.wunderground.com/api/{}/{}/q/{}.json'.format(SECRET_TOKEN, feature_string, zip_code)

response = requests.get(url)

import requests
import sys
import os
import pickle
# import argparse
from weather_lib import Location, Hurricane, Condition
from weather_lib import Forecast, Astronomy, Alert
from secrets import SECRET_TOKEN


zip_code = 92651


def pickle_weather_data(weather_data):
    with open('{}.pickle'.format(weather_data['location']['zip']), 'wb') as f:
        pickle.dump(weather_data, f, pickle.HIGHEST_PROTOCOL)


def get_weather_data(zip_code):
    features = ['astronomy', 'forecast', 'geolookup',
                'conditions', 'currenthurricane', 'alerts']
    feature_string = "{}/{}/{}/{}/{}/{}".format(*features)
    url = "http://api.wunderground.com/api/{}/{}/q/{}.json".format(
                            SECRET_TOKEN, feature_string, zip_code)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Status Code: {}".format(response.status_code))
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def load_or_request_data(zip_code):
    if os.path.isfile('92651.pickle'):
        with open('92651.pickle', 'rb') as f:
            data = pickle.load(f)
        if data['location']['zip'] == zip_code:
            return data
        else:
            return get_weather_data(zip_code)
    else:
        return get_weather_data(zip_code)


def main():
    weather = load_or_request_data(92651)
    print(weather.keys())
    location = Location(**weather['location'])
    print(location)
    if weather['currenthurricane']:
        hurricanes = [Hurricane(**hurricane) for hurricane in weather['currenthurricane']]
        print(hurricanes)
    if weather['alerts']:
        alerts = [Alert(**alert) for alert in weather['alerts']]
        print(alerts)
    astronomy = Astronomy(**weather['sun_phase'])
    print(astronomy)

if __name__ == '__main__':
    main()

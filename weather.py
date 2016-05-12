import requests
import sys
import os
import pickle
import datetime
import argparse
from weather_lib import Location, Hurricane, Condition
from weather_lib import Forecast, Astronomy, Alert
from secrets import SECRET_TOKEN


def is_fresh(zip_code):
    file_mod_time = datetime.datetime.fromtimestamp(
        os.stat('{}.pickle'.format(zip_code)).st_mtime)
    now = datetime.datetime.today()
    max_delta = datetime.timedelta(minutes=30)
    return now-file_mod_time < max_delta


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
    if os.path.isfile('{}.pickle'.format(zip_code)):
        with open('{}.pickle'.format(zip_code), 'rb') as f:
            data = pickle.load(f)
        if data['location']['zip'] == zip_code:
            if is_fresh(zip_code):
                return data
            else:
                data = get_weather_data(zip_code)
                pickle_weather_data(data)
                return data
        else:
            data = get_weather_data(zip_code)
            pickle_weather_data(data)
            return data
    else:
        data = get_weather_data(zip_code)
        pickle_weather_data(data)
        return data


def get_location(weather):
    return Location(**weather['location'])


def get_alerts(weather):
    if weather['alerts']:
        return [Alert(**alert) for alert in weather['alerts']]
    else:
        return []


def get_astronomy(weather):
    return Astronomy(**weather['sun_phase'])


def get_condition(weather):
    return Condition(**weather['current_observation'])


def get_forecast(weather):
    if weather['forecast']['txt_forecast']['forecastday']:
        forecast = {'date': weather['forecast']['txt_forecast']['date']}
        forecast['list'] = [Forecast(**forecast) for forecast in weather['forecast']['txt_forecast']['forecastday']]
        return forecast
    else:
        return []

def get_hurricanes(weather):
    if weather['currenthurricane']:
        hurricanes = [Hurricane(**hurricane) for hurricane in weather['currenthurricane']]
        return hurricanes
    else:
        return []


def print_weather(location, alerts, astronomy, condition, forecast, hurricanes):
    os.system('clear')
    print(location)
    if alerts:
        print(alerts)
    print(astronomy)
    print(condition)
    if forecast:
        print(forecast['date'])
        for entry in forecast['list']:
            print(entry)
    if hurricanes:
        print(hurricanes)


def main(zip_code):
    if len(zip_code) == 5 and zip_code.isdigit():
        weather = load_or_request_data(zip_code)
        location = get_location(weather)
        alerts = get_alerts(weather)
        astronomy = get_astronomy(weather)
        condition = get_condition(weather)
        forecast = get_forecast(weather)
        hurricanes = get_hurricanes(weather)
        print_weather(location, alerts, astronomy,
                      condition, forecast, hurricanes)
    else:
        print("That's not a zip code! Try again.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lookup weather.')
    parser.add_argument('zip_code', type=str, nargs='?', default='92651',
                        help='A 5 digit zip code to find weather data.')
    args = parser.parse_args()
    main(args.zip_code)

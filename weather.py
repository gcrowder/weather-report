import requests
import sys
import os
import pickle
import datetime
import argparse
from weather_lib import Location, Hurricane, Condition
from weather_lib import Forecast, Astronomy, Alert
from secrets import SECRET_TOKEN


def validate_zip_code(weather):
    try:
        weather_zip = weather['location']['zip']
    except KeyError:
        print("That's not a real zip code. Check your digits and try again.")
        sys.exit(1)
    return weather_zip


def is_fresh(zip_code):
    """Check to see if pickled weather data is recent (<30 min old)."""
    file_mod_time = datetime.datetime.fromtimestamp(
        os.stat('{}.pickle'.format(zip_code)).st_mtime)
    now = datetime.datetime.today()
    max_delta = datetime.timedelta(minutes=30)
    return now-file_mod_time < max_delta


def pickle_weather_data(weather):
    """ Serialize weather data to disk to prevent repeated API calls."""
    with open('{}.pickle'.format(weather['location']['zip']), 'wb') as f:
        pickle.dump(weather, f, pickle.HIGHEST_PROTOCOL)


def get_weather_data(zip_code):
    """ Request weather data with given features and return JSON-ified data."""
    features = ['astronomy', 'forecast10day', 'geolookup',
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
    """ Load appropriate pickle and check freshness. Else download data.
        Returns JSON format weather data. """
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
        validate_zip_code(data)
        pickle_weather_data(data)
        return data


def get_location(weather):
    """Return a Location object from the JSON weather data."""
    try:
        location = Location(**weather['location'])
    except KeyError:
        print("That's not a real zip code. Check your digits and try again.")
        sys.exit(1)
    return location


def get_alerts(weather):
    """ Check to see if JSON weather data has any alerts.
        Depending on result, return list of Alert objects or empty list. """
    if weather['alerts']:
        return [Alert(**alert) for alert in weather['alerts']]
    else:
        return []


def get_astronomy(weather):
    """Return an Astronomy object from the JSON weather data."""
    return Astronomy(**weather['sun_phase'])


def get_condition(weather):
    """Return a Condition object from the JSON weather data."""
    return Condition(**weather['current_observation'])


def get_forecast(weather):
    """ Check to see if JSON weather data has any forecasts.
        Depending on result, return list of Forecast objects or empty list. """
    if weather['forecast']['txt_forecast']['forecastday']:
        forecast = {'date': weather['forecast']['txt_forecast']['date']}
        forecast['list'] = [Forecast(**forecast)
                            for forecast in
                            weather['forecast']['txt_forecast']['forecastday']]
        return forecast
    else:
        return []


def get_hurricanes(weather):
    """ Check to see if JSON weather data has any hurricanes.
        Depending on result, return list of Hurricane objects or empty list."""
    if weather['currenthurricane']:
        hurricanes = [Hurricane(**hurricane)
                      for hurricane
                      in weather['currenthurricane']]
        return hurricanes
    else:
        return []


def print_weather(location, alerts, astronomy,
                  condition, forecast, hurricanes):
    """ Clear the screen and print applicable feature objects. """
    os.system('clear')
    print(location)
    if alerts:
        for alert in alerts:
            print(alert)
    print(astronomy)
    print(condition)
    if forecast:
        print(forecast['date'])
        for entry in forecast['list']:
            print(entry)
    if hurricanes:
        for hurricane in hurricanes:
            print(hurricane)


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

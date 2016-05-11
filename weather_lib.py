class Location:

    def __init__(self, location):
        self.city = location['city']
        self.state = location['state']
        self.country_name = location['country_name']
        self.zip = location['zip']

    def __str__(self):
        return "Zip Code {zip}: is in {city}, {state} {country_name}".format(
                                                city=self.city,
                                                state=self.state,
                                                country_name=self.country_name,
                                                zip=self.zip)


class Hurricane:

    def __init__(self, stormInfo):
        self.name = stormInfo["stormName_Nice"]
        self.number = stormInfo["stormNumber"]

    def __str__(self):
        return "{} {}".format(self.name, self.number)


class Conditions:

    def __init__(self, estimated):
        self.weather = estimated['weather']
        self.temperature = estimated['temperature_string']
        self.humidity = estimated['relative_humidity']


class Forecast:

    def __init(self, txt_forecast):
        self.forecast_list = txt_forecast['forecastday']
        self.date = txt_forecast['date']

    def __str__(self):
        return "{} period Forecast at {}".format(len(self.forecast_list),
                                                 self.date)


class Astronomy:

    def __init__(self, sunrise, sunset):
        self.sunsrise = "{}:{}".format(sunrise['hour'], sunrise['minute'])
        self.sunset = "{}:{}".format(sunset['hour'], sunset['minute'])

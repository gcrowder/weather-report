class Alert:
    """ Alert object takes in an alert dictionary from JSON weather data."""
    def __init__(self, **kwargs):
        self.type = kwargs['type']
        self.date = kwargs['date']
        self.description = kwargs['description']
        self.message = kwargs['message']

    def __str__(self):
        return "{type}: {description} {date}\n{message}".format(
                                                type=self.type,
                                                date=self.date,
                                                description=self.description,
                                                message=self.message)


class Location:
    """ Location objects takes a location dict from the JSON weather data."""
    def __init__(self, **kwargs):
        self.city = kwargs['city']
        self.state = kwargs['state']
        self.country_name = kwargs['country_name']
        self.zip = kwargs['zip']

    def __str__(self):
        return "Zip Code {zip} is in {city}, {state} {country_name}".format(
                                                city=self.city,
                                                state=self.state,
                                                country_name=self.country_name,
                                                zip=self.zip)


class Hurricane:
    """ Hurricane object takes a hurricane dict from the JSON weather data."""
    def __init__(self, **kwargs):
        self.name = kwargs["stormName_Nice"]
        self.number = kwargs["stormNumber"]

    def __str__(self):
        return "{} {}".format(self.name, self.number)


class Condition:
    """ Condition takes a weather conditions dict from the JSON data."""
    def __init__(self, **kwargs):
        self.weather = kwargs['weather']
        self.temperature = kwargs['temperature_string']
        self.humidity = kwargs['relative_humidity']

    def __str__(self):
        return "Weather: {}\nTemperature: {}\nHumidity: {}".format(
                        self.weather, self.temperature, self.humidity)


class Forecast:
    """ Forecast takes a forecast dict from the JSON weather data."""
    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self.text = kwargs['fcttext']

    def __str__(self):
        return "{}:\n{}\n".format(self.title, self.text)


class Astronomy:
    """ Astronomy takes a sun_phase dict from the JSON weather data."""
    def __init__(self, **kwargs):
        self.sunrise = "{}:{}".format(kwargs['sunrise']['hour'],
                                      kwargs['sunrise']['minute'])
        self.sunset = "{}:{}".format(kwargs['sunset']['hour'],
                                     kwargs['sunset']['minute'])

    def __str__(self):
        return "Sunrise: {} Sunset: {}".format(self.sunrise, self.sunset)

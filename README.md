# weather-report
This python3 script uses the Weather Underground API to retrieve weather data for a given zip code and print that data to the command line screen.
## Setup:
1. Clone this git repository.
2. Acquire an [API key from the Weather Underground](https://www.wunderground.com/weather/api?apiref=ad8d52019104ddef). Either make a secrets.py file and assign to key to SECRET_TOKEN or assign the key to SECRET_TOKEN in weather.py.
3. Run `python3 weather.py zip_code` where `zip_code` is the zip code you desire.

## Persistence
To save bandwidth (for yourself and the lovely folks at Weather Underground), the data retrieved will be saved as a pickle named `zip_code.pickle`, again where `zip_code` is the number passed to weather.py. If weather.py doesn't find an appropriate pickle or the pickle is stale (older than 30 minutes), weather.py will request the data from Weather Underground.

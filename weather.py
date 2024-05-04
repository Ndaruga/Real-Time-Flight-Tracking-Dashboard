'''
This file will pull the weather data from https://openweatherdata.com for diffrent parameters like city, region etc.

Since we are using the FREE PLAN, we can only query 60 calls/minute and upto 1,000,000 calls/month. 
This means that we should limit our API calls to 23 calls every minute. which implies that we do the any api call after 2.6 seconds

Read more about pricing here https://openweathermap.org/price#weather
'''

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv(override=False)

weather_api_key = os.environ.get('WEATHER_API_KEY')

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?q='

def get_city_weather_data(city_name):
    URL = f"{BASE_URL}{city_name}&appid={weather_api_key}"
    req = requests.get(URL)

    print(req.json())

get_city_weather_data(city_name='Nairobi')



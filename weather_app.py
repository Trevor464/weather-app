import requests
import os
from dotenv import load_dotenv
from sys import exit as ex

def configure():
    load_dotenv()

# Date format: yyyy-MM-dd, e.g. 2010-11-10
def get_weather_info(location:str, date: str = None, end_date: str = None):
    if end_date: end_date = "/" + end_date
    else: date = ""
    if date: date = "/" + date
    else: end_date = ""
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}{date}{end_date}?unitGroup=metric&key={os.getenv('api_key')}"
    response = requests.get(url)

    if (response.status_code == 200):
        return response.json()
    else:
        print(f"Failed to retreive data: ERROR {response.status_code}")
        return None

def main():
    configure()
    print(get_weather_info("woodbridge,ontario", "today"))

main()
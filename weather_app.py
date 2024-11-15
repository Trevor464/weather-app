import requests
import os
from dotenv import load_dotenv
from sys import exit as ex
from nicegui import html, ui
from datetime import datetime

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
    # Functions
    def find_forecast():
        subtitle.set_text(f"Weather forecast from {city.value}, {country.value} on {date.value}")
        info = get_weather_info(f"{city.value},{country.value}", date)
        graph.options["series"][0]["data"] = [h["temp"] for h in info["days"][0]["hours"]]
        graph.update()
        high_and_low.set_text(f"H: {info['days'][0]['tempmax']}  L: {info['days'][0]['tempmin']}")
        sunrise.set_text(f"Sunrise: {info['days'][0]['sunrise']}")
        sunset.set_text(f"Sunset: {info['days'][0]['sunset']}")
        

    configure()

    # Building the UI
    with ui.row().classes("justify-center w-full"):
        with ui.card().classes("col-10"):
            ui.label("Trevor's Weather App").style("font-size: 200%; font-weight: 500px;")
            ui.separator()
            with ui.row().classes("justify-start w-full"):
                with ui.label("Inputs").style("font-size: 150%; font-weight: 500px;").classes("col-3"):
                    city = ui.input(label="City name").style("padding-top: 10px;").props("color=red")
                    country = ui.input(label="Country/region name").style("padding-bottom: 10px").props("color=red")

                    with ui.row().classes("justify-start").style("padding: 30px 0px"):
                        """ ui.checkbox("Single day", value=True,
                                    on_change=lambda e: print(e.value)).classes("col-12").props("color=red") """

                        date = ui.input("Starting date").classes("w-full").props("color=red")
                        """ date2 = ui.input("Ending date").classes("w-full").props("color=red") """

                        with date:
                            with ui.menu().props("no-parent-event") as menu1:
                                with ui.date().props("color=red").bind_value(date):
                                    with ui.row().classes("justify-end"):
                                        ui.button("Close", on_click=menu1.close).props("flat")
                            with date.add_slot("append"):
                                ui.icon("edit_calendar").on("click", menu1.open).classes("cursor-pointer justify-end")
                        """ with date2:
                            with ui.menu().props("no-parent-event") as menu2:
                                with ui.date().props("color=red").bind_value(date2):
                                    with ui.row().classes("justify-end"):
                                        ui.button("Close", on_click=menu2.close).props("flat")
                            with date2.add_slot("append"):
                                ui.icon("edit_calendar").on("click", menu2.open).classes("cursor-pointer justify-end") """
                    
                        ui.button(f"Find forecast", on_click=find_forecast).props("color=red").style("margin-top: 20px; width: 100%")
                with ui.label("Forecast").style("font-size: 150%; font-weight: 500px; margin: 0px 50px").classes("col-7"):
                    subtitle = ui.label("Input an address and a date to get a weather report.").style("font-size: 75%;")

                    # An hourly graph of the temperature
                    graph = ui.echart({
                        "xAxis": {"type": "category", "axisLabel": {":formatter": "value => value + ':00'"}},
                        "yAxis": {"type": "value", "axisLabel": {":formatter": "value => value + '°C'"}},
                        "series": [{"type": "line", "data": [0] * 24}]
                    })

                    ui.label("More data")
                    high_and_low = ui.label("H:  L:").style("font-size: 66%")
                    sunrise = ui.label("Sunrise: ").style("font-size: 66%")
                    sunset = ui.label("Sunset: ").style("font-size: 66%")

    ui.run()

main()

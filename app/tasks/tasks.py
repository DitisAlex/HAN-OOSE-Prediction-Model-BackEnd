import datetime
from . import scheduler
from app.energy import EnergyController
from app.weather import WeatherController


@scheduler.task(
    "interval",
    id="fetch_ev_data",
    seconds=10,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def fetch_ev_data():
    print("running task: Fetching EV data!")
    print(datetime.datetime.now())

    with scheduler.app.app_context():
        ec = EnergyController()
        ec.fetchEnergyData("consumption")
        print("data fetched!")


@scheduler.task(
    "interval",
    id="fetch_pv_data",
    seconds=10,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def fetch_pv_data():
    print("running task: Fetching PV data!")
    print(datetime.datetime.now())

    with scheduler.app.app_context():
        ec = EnergyController()
        ec.fetchEnergyData("production")
        print('data fetched')


# @scheduler.task(
#     "interval",
#     id="fetch_weather_data",
#     hours=1,
#     max_instances=1,
#     start_date="2000-01-01 12:19:00",
# )
# def fetch_weather_data():
#     print("running task: Fetching Weather data!")
#     print(datetime.datetime.now())

#     with scheduler.app.app_context():
#         wc = WeatherController()
#         wc.insertWeatherData()
#         print("data fetched!")

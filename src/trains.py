import pandas as pd
import datetime
from pytz import timezone
from data import Data


class Train():
    stop_id = {
        "from": "de:08311:30306:0:1",
        "to": "de:08311:30306:0:2"
    }
    calendar = {
        0: "T0",
        1: "T0",
        2: "T0",
        3: "T0",
        4: "T0",
        5: "T2",
        6: "T3"
    }

    def __init__(self):
        self.make()

    def make(self):
        try:
            df = pd.read_csv("data/processed/stop_times.csv")
        except FileNotFoundError:
            try:
                df = self.process_data()
            except FileNotFoundError:
                data = Data()
                data.make()
                df = self.process_data()
        self.data = df
        return df

    def process_data(self):
        df = pd.read_csv("data/raw/stop_times.txt", sep=",")
        df = df[df.stop_id == self.stop_id["from"]]
        df.to_csv("data/processed/stop_times.csv", index=False)
        return df



    def get_next(self, data=None):
        if not data:
            data = self.data
        weekday = datetime.datetime.today().weekday()
        trip_id = self.calendar[weekday]
        times = pd.to_datetime(data[(data.trip_id.str.contains(trip_id)) & (data.departure_time < '24:00:00')].departure_time.sort_values().unique())

        now = pd.to_datetime(datetime.datetime.now(timezone("Europe/Berlin")).strftime("%H:%M:00"))

        next_three = pd.to_datetime(times[times > now][:3], format="%H:%M", exact=True)

        next_three = [x.strftime("%H:%M") for x in next_three]

        print(f"Next trains at: {next_three}", flush=True)
        return next_three

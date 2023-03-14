import http.client
import json
from datetime import datetime, timedelta

import plotly.express as px


def get_dates():
    presentday = datetime.now()  # or presentday = datetime.today()
    # Get Tomorrow
    tomorrow = presentday + timedelta(1)
    year = tomorrow.strftime("%d-%m-%Y").split("-")[2]
    month = tomorrow.strftime("%d-%m-%Y").split("-")[1]
    day = tomorrow.strftime("%d-%m-%Y").split("-")[0]
    return year, month, day


if __name__ == "__main__":

    conn = http.client.HTTPSConnection("www.elprisetjustnu.se")
    payload = ""

    year, month, day = get_dates()
    conn.request("GET", "/api/v1/prices/{}/{}-{}_SE3.json".format(year, month, day), payload)
    res = conn.getresponse()

    data = json.loads(res.read().decode())
    fig = px.line(y=[i["SEK_per_kWh"] for i in data], x=[i["time_start"] for i in data])
    fig.write_html("index.html")

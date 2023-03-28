import http.client
import json
from datetime import datetime, timedelta

import plotly.express as px


def get_dates(today):
    presentday = datetime.now()  # or presentday = datetime.today()
    # Get Tomorrow
    if today:
        date = presentday
    else:
        date = presentday + timedelta(1)

    year = date.strftime("%d-%m-%Y").split("-")[2]
    month = date.strftime("%d-%m-%Y").split("-")[1]
    day = date.strftime("%d-%m-%Y").split("-")[0]

    return year, month, day


def api_and_plot(payload, today):

    year, month, day = get_dates(today)
    conn.request("GET", "/api/v1/prices/{}/{}-{}_SE3.json".format(year, month, day), payload)
    res = conn.getresponse()

    if today:
        the_day = "Today"
    else:
        the_day = "Tomorrow"

    data = json.loads(res.read().decode())
    fig = px.line(y=[i["SEK_per_kWh"] for i in data], x=[i["time_start"] for i in data])
    fig.write_html("{}.html".format(the_day))


if __name__ == "__main__":

    conn = http.client.HTTPSConnection("www.elprisetjustnu.se")
    payload = ""

    api_and_plot(payload, today=True)
    api_and_plot(payload, today=False)

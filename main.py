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

    final_price = [item for sublist in [[i["SEK_per_kWh"]]*2 for i in data] for item in sublist]
    final_time = [item for sublist in [[i["time_start"], i["time_end"]] for i in data] for item in sublist]

    px.line(y=final_price, x=final_time)
    fig = px.line(y=[i["SEK_per_kWh"] for i in data], x=[i["time_start"] for i in data])
    fig.update_layout(title='Electricity Spot price for date {}-{}-{}'.format(year, month, day),
                    xaxis_title='Time',
                    yaxis_title='SEK')
    fig.update_yaxes(range=[0.2, 2], row=1, col=1)
    fig.write_html("figures/{}.html".format(the_day))


if __name__ == "__main__":

    conn = http.client.HTTPSConnection("www.elprisetjustnu.se")
    payload = ""

    api_and_plot(payload, today=True)
    api_and_plot(payload, today=False)

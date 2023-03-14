import json
import http.client
import plotly.express as px

if __name__ == "__main__":

    conn = http.client.HTTPSConnection("www.elprisetjustnu.se")
    payload = ""
    conn.request("GET", "/api/v1/prices/2023/03-14_SE3.json", payload)
    res = conn.getresponse()

    data = json.loads(res.read().decode())
    fig = px.line(y=[i["SEK_per_kWh"] for i in data], x=[i["time_start"] for i in data])
    fig.write_html("index.html")
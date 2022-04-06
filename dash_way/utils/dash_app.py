import json
from datetime import datetime

import dash
import plotly
from dash import dcc, html
from dash.dependencies import Input, Output
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.wsgi import WSGIMiddleware

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Ticket Analytics"

server = FastAPI()
server.mount("/", WSGIMiddleware(app.server))

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Ticket Analytics", className="header-title"),
                html.P(
                    children="Analyze the prices of tickets",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Number", className="menu-title"),
                        dcc.Dropdown(
                            id="ticket_num",
                            options=[
                                {
                                    "label": f"ticket_{number}",
                                    "value": f"ticket_{number}",
                                }
                                for number in range(100)
                            ],
                            value="ticket_0",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id="price-chart",
                    config={"displayModeBar": False},
                ),
                dcc.Interval(id="interval-component", interval=1 * 1000, n_intervals=0),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("price-chart", "figure"),
    [Input("interval-component", "n_intervals"), Input("ticket_num", "value")],
)
def update_charts(n, ticket_num):
    with open(f"./data/data.json", "r", encoding="utf-8") as f:
        data: dict = json.load(f)
    fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig.append_trace(
        {
            "x": [
                datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                for ts in data["time"]
            ],
            "y": data[ticket_num],
            "name": ticket_num,
            "mode": "lines+markers",
            "type": "scatter",
        },
        1,
        1,
    )
    return fig

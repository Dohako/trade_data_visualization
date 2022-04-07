from datetime import datetime

import dash
import plotly
from dash import dcc, html
from dash.dependencies import Input, Output
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.wsgi import WSGIMiddleware
from utils.redis_handler import MyRedis

OPERATION_INTERVALS = ("All", "5 last", "10 last", "60 last", "120 last", "300 last")
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
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
                html.Div(
                    children=[
                        html.Div(
                            children="Show operations for next period",
                            className="menu-title",
                        ),
                        dcc.Dropdown(
                            id="show_operations",
                            options=[
                                {
                                    "label": period,
                                    "value": period,
                                }
                                for period in OPERATION_INTERVALS
                            ],
                            value=OPERATION_INTERVALS[1],
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Interval", className="menu-title"),
                        dcc.Input(
                            id="interval",
                            type="range",
                            min=1,
                            max=30,
                            step=1,
                            value=5,
                        ),
                        html.Div(id="interval_value", className="menu-title"),
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
    [
        Output("price-chart", "figure"),
        Output("interval_value", "children"),
        Output("interval-component", "interval"),
    ],
    [
        Input("interval-component", "n_intervals"),
        Input("ticket_num", "value"),
        Input("show_operations", "value"),
        Input("interval", "value"),
    ],
)
def update_charts(n, ticket_num, show_operations: str, interval: int):

    r = MyRedis()
    if show_operations != OPERATION_INTERVALS[0]:
        from_value = -int(show_operations.split()[0])
    else:
        from_value = 0
    fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig.append_trace(
        {
            "x": [
                datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                for ts in r.get_list_from_redis("time", from_value)
            ],
            "y": r.get_list_from_redis(ticket_num, from_value),
            "name": ticket_num,
            "mode": "lines+markers",
            "type": "scatter",
        },
        1,
        1,
    )
    return fig, interval, int(interval) * 1000

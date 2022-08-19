from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids


def render(app: Dash, escritorios: list) -> html.Div:
    # all_nations = ["South Korea", "China", "Canada"]

    return html.Div(
        children=[
            # html.H6("Nation"),
            dcc.Dropdown(
                id=ids.SELECT_ESCRITORIO,
                options=[{"label": nation, "value": nation} for nation in escritorios],
                value=escritorios[0],
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_NATIONS_BUTTON,
                n_clicks=0,
            ),
        ],
    )

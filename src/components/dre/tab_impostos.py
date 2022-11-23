from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from src.components import ids


style1 = {
    "textAlign": "center",
}


def tab_impostos():
    return html.Div(
        dbc.Row(
            dbc.Col([
                dcc.Graph(id=ids.PIE_IMP),
            ]),
        )
    )


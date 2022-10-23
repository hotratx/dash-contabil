from dash import Dash, html, dcc
from . import ids


class SelectOne:
    def __init__(self, app: Dash):
        self._app = app

    def render(self, options: list) -> html.Div:
        self.options = options

        return html.Div(
            children=[
                dcc.Dropdown(
                    options=[{"label": value, "value": value} for value in self.options],
                    value=self.options[0],
                    multi=False,
                ),
            ],
        )

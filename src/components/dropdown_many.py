from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids


class SelectMany:
    def __init__(self, app: Dash):
        self._app = app
        self.callback()

    def callback(self):
        @self._app.callback(
            Output(ids.SELECT_MANY, "value"),
            Input(ids.SELECT_ALL, "n_clicks"),
        )
        def select_all_options(n_clicks):
            if n_clicks:
                return self.options

    def render(self, options: list) -> html.Div:
        self.options = options

        return html.Div(
            children=[
                dcc.Dropdown(
                    id=ids.SELECT_MANY,
                    options=[{"label": nation, "value": nation} for nation in self.options],
                    value=self.options[0],
                    multi=True,
                ),
                html.Button(
                    className="dropdown-button",
                    children=["Select All"],
                    id=ids.SELECT_ALL,
                    n_clicks=0,
                ),
            ],
        )

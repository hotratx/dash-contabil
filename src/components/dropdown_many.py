from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids


class SelectManyA:
    def __init__(self, app: Dash):
        self._app = app
        self.callback()

    def callback(self):
        @self._app.callback(
            Output(ids.SELECT_MANYA, "value"),
            Input(ids.SELECT_ALLA, "n_clicks"),
        )
        def select_all_options(n_clicks):
            if n_clicks:
                return self.options

    def render(self, options: list) -> html.Div:
        self.options = options

        return html.Div(
            children=[
                dcc.Dropdown(
                    id=ids.SELECT_MANYA,
                    options=[{"label": nation, "value": nation} for nation in options],
                    value=options[0],
                    multi=True,
                ),
                html.Button(
                    className="dropdown-button",
                    children=["Select All"],
                    id=ids.SELECT_ALLA,
                    n_clicks=0,
                ),
            ],
        )


class SelectManyB:
    def __init__(self, app: Dash):
        self._app = app
        self.callback()

    def callback(self):
        @self._app.callback(
            Output(ids.SELECT_MANYB, "value"),
            Input(ids.SELECT_ALLB, "n_clicks"),
        )
        def select_all_options(n_clicks):
            if n_clicks:
                print(f'SELECE ALLLLLLLLLLLLLLLLLLLL: {self.options}')
                return self.options

    def render(self, options: list) -> html.Div:
        self.options = options

        return html.Div(
            children=[
                dcc.Dropdown(
                    id=ids.SELECT_MANYB,
                    options=[{"label": nation, "value": nation} for nation in options],
                    value=options[0],
                    multi=True,
                ),
                html.Button(
                    className="dropdown-button",
                    children=["Select All"],
                    id=ids.SELECT_ALLB,
                    n_clicks=0,
                ),
            ],
        )

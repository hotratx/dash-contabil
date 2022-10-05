from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids


class SelectEscritorios:
    def __init__(self, app: Dash):
        self._app = app
        self._run()

    def _run(self):
        @self._app.callback(
            Output(ids.SELECT_ESCRITORIO_ADD_USER, "value"),
            Input(ids.SELECT_ALL_NATIONS_BUTTON, "n_clicks"),
        )
        def select_all_nations(n_clicks):
            if n_clicks:
                print(f'DENTRO DO SELECT {self._esc}')
                return self._esc


    def render(self, esc) -> html.Div:
        self._esc = esc

        return html.Div(
            children=[
                # html.H6("Nation"),
                dcc.Dropdown(
                    id=ids.SELECT_ESCRITORIO_ADD_USER,
                    options=[{"label": nation, "value": nation} for nation in esc],
                    value=esc[0],
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

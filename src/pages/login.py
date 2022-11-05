from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from src.database import Crud
from src.password import verify_password
from flask_login import login_user, UserMixin
from dash.exceptions import PreventUpdate
from src.components import ids


CARD_STYLE = {
    "width": "300px",
    "min-height": "300px",
    "padding-right": "25px",
    "padding-top": "25px",
    "padding-left": "25px",
    "align-self": "center",
}


class User(UserMixin):
    def __init__(self, username):
        self.id = username


class PageLogin:
    def __init__(self, app: Dash):
        self._app = app
        self._run()
        self.crud = Crud()

    def _run(self):
        @self._app.callback(
            Output(ids.URL_LOGIN, "pathname"),
            Output(ids.OUTPUT_STATE, "children"),
            [Input(ids.LOGIN_BTN, "n_clicks")],
            [State(ids.USER_LOGIN, "value"), State(ids.PWD_LOGIN, "value")],
        )
        def login_button_click(n_clicks, username, password):
            """Callback do component Login"""
            if n_clicks > 0:
                user_model = self.crud.get_user(username)
                if user_model and password:
                    hash = verify_password(password, user_model.password)
                    if hash:
                        user = User(user_model.username)
                        login_user(user)
                        return ("/home", "")

                return ("/login", "Incorrect username or password")
            raise PreventUpdate

    def render(self):
        card = dbc.Card(
            [
                dcc.Location(id=ids.URL_LOGIN, refresh=True),
                html.Legend("Login", style={"padding-top": "20px"}),
                dbc.Input(
                    id=ids.USER_LOGIN,
                    placeholder="Username",
                    type="text",
                    style={"margin-top": "10px"},
                ),
                dbc.Input(
                    id=ids.PWD_LOGIN,
                    placeholder="Password",
                    type="password",
                    style={"margin-top": "10px"},
                ),
                dbc.Button(
                    "Login",
                    n_clicks=0,
                    id=ids.LOGIN_BTN,
                    style={"margin-top": "10px"},
                ),
                html.Span(
                    id=ids.OUTPUT_STATE,
                    style={"text-align": "center", "margin-top": "10px"},
                ),
                html.Br(),
            ],
            style=CARD_STYLE,
        )

        login = dbc.Container(
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    card,
                                    style={
                                        "height": "100vh",
                                        "display": "flex",
                                        "justify-content": "center",
                                    },
                                ),
                            ]
                        )
                    ]
                ),
            ],
            fluid=True,
        )
        return login

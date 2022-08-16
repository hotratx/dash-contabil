from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from src.database.crud import CRUDUser
from src.password import verify_password
from flask_login import login_user, UserMixin
from dash.exceptions import PreventUpdate


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


class Login:
    def __init__(self, app: Dash):
        self._app = app
        self._run()

    def _run(self):
        @self._app.callback(
            Output("url_login", "pathname"),
            Output("output-state", "children"),
            [Input("login-btn", "n_clicks")],
            [State("user-login", "value"), State("pwd-login", "value")],
        )
        def login_button_click(n_clicks, username, password):
            """Callback do component Login"""
            if n_clicks > 0:
                u = CRUDUser()
                user_model = u.get(username)
                if user_model and password:
                    hash = verify_password(password, user_model.password)
                    user = User(user_model.username)
                    if hash:
                        login_user(user)
                        return ("/home", "")

                return ("/login", "Incorrect username or password")
            raise PreventUpdate

    def render(self):
        login = dbc.Card(
            [
                dcc.Location(id="url_login", refresh=True),
                html.Legend("Login", style={"padding-top": "20px"}),
                dbc.Input(
                    id="user-login",
                    placeholder="Username",
                    type="text",
                    style={"margin-top": "10px"},
                ),
                dbc.Input(
                    id="pwd-login",
                    placeholder="Password",
                    type="password",
                    style={"margin-top": "10px"},
                ),
                dbc.Button(
                    "Login",
                    n_clicks=0,
                    id="login-btn",
                    style={"margin-top": "10px"},
                ),
                html.Span(
                    id="output-state",
                    style={"text-align": "center", "margin-top": "10px"},
                ),
                html.Br(),
            ],
            style=CARD_STYLE,
        )
        return login

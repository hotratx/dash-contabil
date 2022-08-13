from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from flask_login import login_user, UserMixin, logout_user, current_user
from src.pages import home, login
from src.database.crud import CRUDUser
from src.password import get_password_hash, verify_password


class User(UserMixin):
    def __init__(self, username):
        self.id = username


def create_layout(app: Dash) -> dbc.Container:
    @app.callback(
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

    @app.callback(
        Output("url_logout", "pathname"), Input("logout-btn", "n_clicks")
    )
    def logout_button_click(n_clicks):
        """Callback controle de páginas"""
        if n_clicks > 0:
            return "/logout"

    @app.callback(
        Output("page-content", "children"),
        Input("base-url", "pathname"),
    )
    def render_page_content(pathname):
        """Callback controle de páginas"""
        if pathname == "/login" or pathname == "/":
            return login.render()
        elif pathname == "/home":
            if current_user.is_authenticated:
                return home.render(app)
            else:
                return login.render()
        elif pathname == "/logout":
            print("ENTROU NO LOGOUT")
            if current_user.is_authenticated:
                logout_user()
                return login.render()

    main = dbc.Container(
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Location(id="base-url", refresh=False),
                            html.Div(
                                id="page-content",
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

    return main

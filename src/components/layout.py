from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from flask_login import login_user, UserMixin, logout_user, current_user
from src.pages.home import Home
from src.pages.login import Login
from src.database.crud import CRUDUser
from src.password import get_password_hash, verify_password



class User(UserMixin):
    def __init__(self, username):
        self.id = username


def create_layout(app: Dash) -> dbc.Container:
    login = Login(app)
    home = Home(app)

    # @app.callback(
    #     Output("url_logout", "pathname"), Input("logout-btn", "n_clicks")
    # )
    # def logout_button_click(n_clicks):
    #     """Callback controle de páginas"""
    #     if n_clicks > 0:
    #         return "/logout"

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
                return home.render()
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

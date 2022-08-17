from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from flask_login import logout_user, current_user
from src.pages.home import Home
from src.pages.login import Login
from src.components import ids


def create_layout(app: Dash) -> html.Div:
    login = Login(app)
    home = Home(app)

    @app.callback(
        Output(ids.PAGE_CONTENT, "children"),
        Input(ids.BASE_URL, "pathname"),
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
    main = html.Div(

        dcc.Location(id=ids.BASE_URL, refresh=False),
        id=ids.PAGE_CONTENT,
    )
    return main

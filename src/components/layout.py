from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from flask_login import logout_user, current_user
from src.pages import PageLogin
from src.components.sidebar import Sidebar
from src.components import ids


def create_layout(app: Dash) -> html.Div:
    login = PageLogin(app)
    sidebar = Sidebar(app)

    @app.callback(
        Output(ids.PAGE_CONTENT, "children"),
        Input(ids.BASE_URL, "pathname"),
    )
    def render_page_content(pathname):
        """Callback controle de páginas"""
        home = ['/home', '/page-1', '/page-2', '/page-3']
        if pathname == "/login" or pathname == "/":
            return login.render()
        elif pathname in home:
            if current_user.is_authenticated:
                return sidebar.render()
            else:
                return login.render()
        elif pathname == "/logout":
            print("ENTROU NO LOGOUT")
            if current_user.is_authenticated:
                logout_user()
                return login.render()
        else:
            return html.Div(
                [
                    html.H1("404: Not found", className="text-danger"),
                    html.Hr(),
                    html.P(f"The pathname {pathname} was not recognised..."),
                ]
            )

    main = html.Div(
        dcc.Location(id=ids.BASE_URL, refresh=False),
        id=ids.PAGE_CONTENT,
    )
    return main

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from src.pages import login, home



def create_layout(app: Dash) -> dbc.Container:
    @app.callback(
            Output("page-content", "children"),
            Input("base-url", "pathname"),
    )
    def render_page_content(pathname):
        if (pathname == "/login" or pathname == "/"):
            return login.render()
        elif (pathname == "/home"):
            return home.render(app)

    return dbc.Container(children=[
            dbc.Row([
                dbc.Col([
                    dcc.Location(id="base-url", refresh=False),
                    html.Div(id="page-content", style={'height': '100vh', 'display': 'flex', 'justify-content': 'center'}),
                    ])
            ]),
            ], fluid=True)


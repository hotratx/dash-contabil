from dash import Dash, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from src.pages import PageConfig, PageDRE, PageAdmin
from flask_login import current_user
from src.database import Crud
from . import ids


PLOTLY_LOGO = "https://cdn-icons-png.flaticon.com/128/786/786395.png"


class Sidebar:
    def __init__(self, app: Dash):
        self._app = app
        self._config = PageConfig(app)
        self.analise = PageDRE(app)
        self.admin = PageAdmin(app)
        self._crud = Crud()
        self._run()

    def _run(self):
        @self._app.callback(
            [
                Output("sidebar", "style"),
                Output("page-content-sidebar", "style"),
                Output("side_click", "data"),
            ],
            [Input("btn_sidebar", "n_clicks")],
            [
                State("side_click", "data"),
            ],
        )
        def toggle_sidebar(n, nclick):
            if n:
                if nclick == "SHOW":
                    sidebar_style = SIDEBAR_HIDEN
                    content_style = CONTENT_STYLE1
                    cur_nclick = "HIDDEN"
                else:
                    sidebar_style = SIDEBAR_STYLE
                    content_style = CONTENT_STYLE
                    cur_nclick = "SHOW"
            else:
                sidebar_style = SIDEBAR_HIDEN
                content_style = CONTENT_STYLE1
                cur_nclick = "HIDDEN"

            return sidebar_style, content_style, cur_nclick

        @self._app.callback(
            [Output(f"page-{i}-link", "active") for i in range(1, 4)],
            [Input("url", "pathname")],
        )
        def toggle_active_links(pathname):
            if pathname == "/home":
                return True, False, False
            return [pathname == f"/page-{i}" for i in range(1, 4)]

        @self._app.callback(Output("page-content-sidebar", "children"), [Input("url", "pathname")])
        def render_page_content(pathname):
            if pathname in ["/", "/home", "/page-1"]:
                return self.analise.render()
            elif pathname == "/dados":
                return self._config.render()
            elif pathname == "/admin":
                user = self._crud.get_user(current_user.get_id())
                if user.is_admin:
                    return self.admin.render()
                return html.P("Only admin!")

        @self._app.callback(Output("url", "pathname"), Input(ids.LOGOUT_BTN, "n_clicks"))
        def logout_button_click(n_clicks):
            """Callback controle de páginas"""
            if n_clicks > 0:
                return "/logout"

    def render(self):
        logout = dbc.Row(
            [
                dbc.Col(html.Span(f"user: {current_user.get_id()}", style={"margin-left": "-90px", "color": "white"})),
                dbc.Col(
                    dbc.Button(
                        "Sair",
                        id=ids.LOGOUT_BTN,
                        color="primary",
                        className="ms-2",
                        n_clicks=0,
                        style={"margin-right": "-70px"},
                    ),
                    width="auto",
                ),
            ],
            className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
            align="center",
        )
        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                # dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
                                dbc.Col(
                                    dmc.ActionIcon(
                                        DashIconify(icon="clarity:settings-line"), variant="default", id="btn_sidebar", n_clicks=0, style={"margin-left": "-60px"}
                                    ),
                                ),
                                # dbc.Col(
                                #     html.Img(
                                #         id="btn_sidebar", src=PLOTLY_LOGO, height="30px", style={"margin-left": "-70px"}
                                #     )
                                # ),
                                dbc.Col(dbc.NavbarBrand("Contábil", style={"margin-left": "-25px"})),
                            ],
                            align="left",
                            className="g-0",
                        ),
                        # href="https://plotly.com",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                    dbc.Collapse(
                        logout,
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True,
                    ),
                ]
            ),
            color="dark",
            dark=True,
        )
        sidebar = html.Div(
            [
                html.Hr(),
                dbc.Nav(
                    [
                        dbc.NavLink("Gráficos", href="/home", id="page-1-link"),
                        dbc.NavLink("Adicionar dados", href="/dados", id="page-2-link"),
                        dbc.NavLink("Admin", href="/admin", id="page-3-link"),
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],
            id="sidebar",
            style=SIDEBAR_HIDEN,
        )

        content = html.Div(id="page-content-sidebar", style=CONTENT_STYLE1)

        layout = html.Div(
            [
                dcc.Store(id="side_click"),
                dcc.Location(id="url"),
                navbar,
                sidebar,
                content,
            ],
        )
        return layout


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 77,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 77,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

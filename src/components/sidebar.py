from dash import Dash, html, dcc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from . import ids
from src.pages.home import Home


# PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
PLOTLY_LOGO = "https://cdn-icons-png.flaticon.com/128/786/786395.png"


class Sidebar:
    def __init__(self, app: Dash):
        self._app = app
        self._home = Home(app)
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
            ]
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
                sidebar_style = SIDEBAR_STYLE
                content_style = CONTENT_STYLE
                cur_nclick = 'SHOW'

            return sidebar_style, content_style, cur_nclick

        @self._app.callback(
            [Output(f"page-{i}-link", "active") for i in range(1, 4)],
            [Input("url", "pathname")],
        )
        def toggle_active_links(pathname):
            if pathname == "/":
                # Treat page 1 as the homepage / index
                return True, False, False
            return [pathname == f"/page-{i}" for i in range(1, 4)]

        @self._app.callback(Output("page-content-sidebar", "children"), [Input("url", "pathname")])
        def render_page_content(pathname):
            if pathname in ["/", "/page-1"]:
                return html.P("This is the content of page 1!")
            elif pathname == "/page-2":
                # return html.P("This is the content of page 2. Yay!")
                return self._home.render()
            elif pathname == "/page-3":
                return html.P("Oh cool, this is page 3!")
            return html.P("Oh cool, this is page 3!")
            # If the user tries to reach a different page, return a 404 message
            # return dbc.Jumbotron(
            #     [
            #         html.H1("404: Not found", className="text-danger"),
            #         html.Hr(),
            #         html.P(f"The pathname {pathname} was not recognised..."),
            #     ]
            # )

    def render(self):
        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                # dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
                                dbc.Col(html.Img(id="btn_sidebar", src=PLOTLY_LOGO, height="30px")),
                                dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                            ],
                            align="left",
                            className="g-0",
                        ),
                        # href="https://plotly.com",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                    dbc.Collapse(
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True,
                    ),
                ]
            ),
            color="dark",
            dark=True,
        )
        # navbar = dbc.NavbarSimple(
        #     children=[
        #         dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
        #         dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        #         dbc.DropdownMenu(
        #             children=[
        #                 dbc.DropdownMenuItem("More pages", header=True),
        #                 dbc.DropdownMenuItem("Page 2", href="#"),
        #                 dbc.DropdownMenuItem("Page 3", href="#"),
        #             ],
        #             nav=True,
        #             in_navbar=True,
        #             label="More",
        #         ),
        #     ],
        #     brand="Brand",
        #     brand_href="#",
        #     color="dark",
        #     dark=True,
        #     fluid=True,
        # )

        sidebar = html.Div(
            [
                html.H4("Sidebar", className="display-4"),
                html.Hr(),
                html.P(
                    "A simple sidebar layout with navigation links", className="lead"
                ),
                dbc.Nav(
                    [
                        dbc.NavLink("Page 1", href="/page-1", id="page-1-link"),
                        dbc.NavLink("Page 2", href="/page-2", id="page-2-link"),
                        dbc.NavLink("Page 3", href="/page-3", id="page-3-link"),
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],
            id="sidebar",
            style=SIDEBAR_STYLE,
        )

        content = html.Div(
            id="page-content-sidebar",
            style=CONTENT_STYLE)


        layout = html.Div(
            [
                dcc.Store(id='side_click'),
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
    "top": 62.5,
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
    "top": 62.5,
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

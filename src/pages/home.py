from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import current_user
import dash_bootstrap_components as dbc
from src.handle_pdf import HandlePdf
from src.components.upload import Upload
from src.components import ids
from src.database import Crud


handle_pdf = HandlePdf("db")


class Home:
    def __init__(self, app: Dash):
        self._app = app
        self._upload = Upload(app)
        self._crud = Crud()
        self._run()

    def _escritorios(self):
        try:
            return self._crud.get_escritorios(current_user.get_id()).name
        except Exception:
            return []

    def _run(self):
        @self._app.callback(
            Output(ids.DUMMY, "children"),
            [Input(ids.HANDLE_PDF, "n_clicks")],
        )
        def analise_pdf(n_clicks):
            """Callback controle de páginas"""
            if n_clicks > 0:
                handle_pdf.run()
            raise PreventUpdate

        # @self._app.callback(Output(ids.URL_LOGOUT, "pathname"), Input(ids.LOGOUT_BTN, "n_clicks"))
        # def logout_button_click(n_clicks):
        #     """Callback controle de páginas"""
        #     print("saindo SAINDO")
        #     if n_clicks > 0:
        #         return "/logout"

    def render(self) -> html.Div:
        home = html.Div(
            className="app-div",
            children=[
                html.H1(self._app.title),
                html.Hr(),
                dbc.Button("Logout", id=ids.LOGOUT_BTN, n_clicks=0, color="dark"),
                self._upload.render(),
                html.Div(id=ids.OUTPUT_DATA_UPLOAD),
                dbc.Button("Analisar pdf", id=ids.HANDLE_PDF, n_clicks=0, color="dark"),
                html.P(id=ids.DUMMY),
            ],
        )
        return home

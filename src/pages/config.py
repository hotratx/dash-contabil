from dash import Dash, html, dcc
import dash_mantine_components as dmc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import current_user
import dash_bootstrap_components as dbc
from src.handle_pdf import HandlePdf
from src.components.upload import Upload
from src.components.dropdown_many import SelectManyA, SelectManyB
from src.components import ids
from src.database import Crud


class PageConfig:
    def __init__(self, app: Dash):
        self._app = app
        self._upload = Upload(app)
        self._crud = Crud()
        self._handle_pdf = HandlePdf(self._crud)
        self._revert_value_to_label = {}
        self._run()

    def _escritorios(self):
        escs = self._crud.get_escritorios_from_user(current_user.get_id())
        i = 0
        for e in escs:
            self._revert_value_to_label[i] = e.name
            i += 1

        return [{"label": es.name, "value": value} for es, value in zip(escs, range(len(escs)))]

    def get_all_users(self):
        users = self._crud.get_all_users()
        usuarios = [user.username for user in users]
        return usuarios

    def _all_escritorios_list(self):
        escs = self._crud.get_escritorios_from_user(current_user.get_id())
        resp = []
        for e in escs:
            resp.append(e.name)
        return resp

    def _all_escritorios(self):
        try:
            escs = self._crud.get_escritorios_from_user(current_user.get_id())
            resp = ""
            for e in escs:
                resp += f"{e.name}, "
            self._all_escs = resp
            return resp
        except Exception:
            return ["adf", "sd"]

    def _all_users(self) -> list:
        resp = []
        try:
            users = self._crud.get_all_users()
            for user in users:
                user = self._crud.get_escritorios_and_users_from_user(user.username)
                escritorios = ""
                for esc in user.escritorios:
                    escritorios = escritorios + f" {esc.name} -"
                escritorios = escritorios[:-2]

                resp.append([user.username, escritorios])
            return resp
        except Exception:
            return ["", ""]

    def _run(self):
        @self._app.callback(
            Output(ids.SPINNER, "children"),
            Input(ids.HANDLE_PDF_TBN, "n_clicks"),
            State(ids.SELECT_ESCRITORIO, "value"),
        )
        def analise_pdf(n_clicks, escritorio):
            """Callback controle de páginas"""
            if isinstance(escritorio, str):
                name = self._revert_value_to_label.get(int(escritorio))
                if n_clicks > 0:
                    if escritorio:
                        crud = HandlePdf(self._crud)
                        resp = crud.run(name)
                        response = []
                        for x in resp:
                            response.append(html.P(x))
                        response = response
                        return f"Foi feito o upload dos seguintes arquivos:\n{response}"
                    return "Seleciona um escritório!"
            raise PreventUpdate


    def render(self) -> html.Div:

        # inicio dash_table
        # table2 = dt.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

        # inicio table

        tab1_content = dbc.Card(
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            dbc.CardBody(
                                [
                                    html.P("Arraste ou selecione os pdf par fazer o upload.", className="card-text"),
                                    self._upload.render(),
                                    html.Div(id=ids.OUTPUT_DATA_UPLOAD),
                                ]
                            ),
                        )
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.P(
                                    "Após fazer o upload selecione o escritório e clique em extrair os dados para realizar extração e salvar os dados no banco de dados",
                                    className="card-text",
                                ),
                                html.P("Selecione o escritorio:", className="card-text"),
                                dbc.Select(
                                    id=ids.SELECT_ESCRITORIO,
                                    options=self._escritorios(),
                                    # value=self._escritorios()[0]
                                ),
                                dbc.Button(
                                    "Extrair dados", id=ids.HANDLE_PDF_TBN, n_clicks=0, style={"margin-top": "20px"}
                                ),
                                dbc.Spinner(
                                    html.Div(id=ids.SPINNER, style={"margin-top": "20px"}),
                                    color="primary",
                                    spinner_style={"width": "2rem", "height": "2rem", "margin-top": "-53px"},
                                ),
                            ]
                        ),
                    ),
                ]
            ),
            className="mt-3",
        )

        tabs = html.Div(
            id="tabs",
            className="tabs",
            children=[
                dcc.Tabs(
                    id="app-tabs",
                    value="tab1",
                    className="custom-tabs",
                    children=[
                        dcc.Tab(
                            tab1_content,
                            id="Specs-tab",
                            label="Adicionar Dados",
                            value="tab1",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                    ],
                )
            ],
        )

        home = html.Div(
            className="app-div",
            children=[
                html.H1("Add dados:"),
                html.Hr(),
                # dcc.Markdown(children=markdown_text),
                tabs,
            ],
            style={"background-color": "#f8f9fa"},
        )
        return home

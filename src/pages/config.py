import time
from dash import Dash, html, dcc
import dash_table as dt
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import current_user
import dash_bootstrap_components as dbc
from src.handle_pdf import HandlePdf
from src.components.upload import Upload
from src.components.dropdown_many import SelectMany
from src.components import ids
from src.database import Crud

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')


class PageConfig:
    def __init__(self, app: Dash):
        self._app = app
        self._upload = Upload(app)
        self._crud = Crud()
        self._handle_pdf = HandlePdf(self._crud)
        self.select_many = SelectMany(app)
        self._revert_value_to_label = {}
        self._run()

    def _escritorios(self):
        escs = self._crud.get_escritorios_from_user(current_user.get_id())
        i = 0
        for e in escs:
            self._revert_value_to_label[i] = e.name
            i += 1

        return [{'label': es.name, 'value': value} for es, value in zip(escs, range(len(escs)))]

    def get_all_users(self):
        users = self._crud.get_all_users()
        return [user.username for user in users]

    def _all_escritorios_list(self):
        escs = self._crud.get_escritorios_from_user(current_user.get_id())
        resp = []
        for e in escs:
            resp.append(e.name)
        return resp

    def _all_escritorios(self):
        try:
            escs = self._crud.get_escritorios_from_user(current_user.get_id())
            resp = ''
            for e in escs:
                resp += f'{e.name}, '
            self._all_escs = resp
            return resp
        except Exception:
            return ['adf', 'sd']

    def _all_users(self) -> list:
        try:
            escs = self._crud.get_escritorios_from_user(current_user.get_id())
            all_users = []
            for esc in escs:
                for user in esc.users:
                    all_users.append([user.username, esc.name])
            return all_users
        except Exception:
            return ['adf', 'sd']


    def _run(self):
        @self._app.callback(
            Output(ids.SPINNER, "children"),
            Input(ids.HANDLE_PDF_TBN, "n_clicks"),
            State(ids.SELECT_ESCRITORIO, "value"),
        )
        def analise_pdf(n_clicks, escritorio):
            """Callback controle de páginas"""
            print(f'ANALISE PDF escritorio: {type(escritorio)}\nvalue escritorio: {escritorio}')
            if isinstance(escritorio, str):
                print(f'TYPE _revert_value_to_label: {type(self._revert_value_to_label)}')
                print(f'VALUE _revert_value_to_label: {self._revert_value_to_label}')
                name = self._revert_value_to_label.get(int(escritorio))
                print(f'NAME: {name}')
                if n_clicks > 0:
                    print('vai chamar o handepdf')
                    resp = self._handle_pdf.run(name)
                    response = []
                    for x in resp:
                        response.append(html.P(x))
                    response = response
                    return f"Foi feito o upload dos seguintes arquivos:\n{response}"
            raise PreventUpdate

        @self._app.callback(
            Output(ids.ALERT_NEW_USER_SUCESS, "is_open"),
            Output(ids.ALERT_NEW_USER_ERROR, "is_open"),
            [Input(ids.SUBMIT_NEW_USER, "n_clicks")],
            [State(ids.NEW_USERNAME, "value"), State(ids.NEW_PASSWORD, "value"), State(ids.SELECT_MANY, 'value'), State(ids.ALERT_NEW_USER_SUCESS, 'is_open')],
        )
        def add_new_user(n_clicks, username, password, escritorio, is_open):
            """Callback controle de páginas"""
            print(f'NAMENAMENAMENAMENAME --- USERNAME: {username} - PASSWORD: {password} - ESCRITORIO: {escritorio}')
            # print(f'{self._revert_value_to_label[int(escritorio[0])]}')
            if n_clicks > 0:
                print('PASSOU DO n_clicks')
                if username and password:
                    print('VAI PRO BANCO DE DADOS')
                    # resp = self._crud.add_user([self._revert_value_to_label[int(escritorio[0])]], username, password)
                    # print(f'RESPONSE DO CRUD: {resp}')
                    return not is_open, is_open
                else:
                    return is_open, not is_open
            return is_open, is_open

        @self._app.callback(
            Output(ids.ALERT_NEW_ESCRITORIO_SUCESS, "is_open"),
            Output(ids.ALERT_NEW_ESCRITORIO_ERROR, "is_open"),
            [Input(ids.SUBMIT_NEW_ESCRITORIO, "n_clicks")],
            State(ids.NEW_ESCRITORIO, "value"),
            State(ids.SELECT_ALL, 'value'),
            State(ids.ALERT_NEW_ESCRITORIO_SUCESS, "is_open")
        )
        def add_new_escritorio(n_clicks, value, users, is_open):
            """Callback controle de páginas"""
            if n_clicks > 0:
                if value:
                    print(f'XXXXXXX\nn_clicks: {n_clicks}, users: {users}, value: {value}, is_open: {is_open}')
                    # e = self._crud.add_escritorio(value, current_user.get_id())
                    # print(f'SUCESSO ADD NOVO ESCRIORIO: {e}')
                    self._all_escritorios()
                    return not is_open, is_open
                else:
                    return is_open, not is_open
            return is_open, is_open

    def render(self) -> html.Div:
        name_escritorio = dbc.Row(
            [
                dbc.Label("Name", html_for="example-text-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id=ids.NEW_ESCRITORIO, placeholder="Nome do escritório"
                    ),
                    width=10,
                ),
            ],
            className="mb-3",
        )

        users_input = dbc.Row(
            [
                dbc.Label("Usuários", html_for="example-password-row", width=2),
                dbc.Col(
                    self.select_many.render(self.get_all_users())
                )
            ],
            className="mb-3",
        )

        username_input = dbc.Row(
            [
                dbc.Label("Username", html_for="example-text-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id=ids.NEW_USERNAME, placeholder="Enter username"
                    ),
                    width=10,
                ),
            ],
            className="mb-3",
        )

        password_input = dbc.Row(
            [
                dbc.Label("Password", html_for="example-password-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="password",
                        id=ids.NEW_PASSWORD,
                        placeholder="Enter password",
                    ),
                    width=10,
                ),
            ],
            className="mb-3",
        )

        escritorio_input = dbc.Row(
            [
                dbc.Label("Escritório", html_for="example-password-row", width=2),
                dbc.Col(
                    # escritorios_dropdown.render(self._app, self._all_escritorios_list()),
                    self.select_many.render(self._all_escritorios_list())
                )
            ],
            className="mb-3",
        )

        # inicio dash_table
        # table2 = dt.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])



        # inicio table
        table_header = [
            html.Thead(html.Tr([html.Th("Usuário"), html.Th("Escritório")]))
        ]

        data = []
        for x in self._all_users():
            data.append(html.Tr([html.Td(x[0]), html.Td(x[1])]))
        table_body = [html.Tbody(data)]
        print(f'ALLLLLLL TABLESSS: {data}')

        table = dbc.Table(table_header + table_body, bordered=True, style={'margin-top': '20px',  'display': 'inline-block', 'width': '100%'})
        # fim table

        tab1_content = dbc.Card(
            dbc.Row(
                [
                    dbc.Col(html.Div(
                        dbc.CardBody(
                            [
                                html.P("Arraste ou selecione os pdf par fazer o upload.", className="card-text"),
                                self._upload.render(),
                                html.Div(id=ids.OUTPUT_DATA_UPLOAD),
                            ]
                        ),

                    )),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.P("Após fazer o upload selecione o escritório e clique em extrair os dados para realizar extração e salvar os dados no banco de dados", className="card-text"),
                                html.P("Selecione o escritorio:", className="card-text"),
                                dbc.Select(
                                    id=ids.SELECT_ESCRITORIO,
                                    options=self._escritorios(),
                                    # value=self._escritorios()[0]

                                ),
                                dbc.Button("Extrair dados", id=ids.HANDLE_PDF_TBN, n_clicks=0, style={'margin-top': '20px'}),
                                dbc.Spinner(html.Div(id=ids.SPINNER, style={'margin-top': '20px'}), color="primary", spinner_style={"width": "2rem", "height": "2rem", "margin-top": "-53px"}),
                            ]
                        ),
                    ),
                ]
            ),

            className="mt-3"
        )

        tab2_content = dbc.Card(
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardBody(
                        [
                            dbc.Form([username_input, password_input, escritorio_input]),
                            dbc.Row(
                                dbc.Col([
                                    dbc.Button("Submit", id=ids.SUBMIT_NEW_USER, n_clicks=0, style={'margin-top': '20px', "justify-content": "center"}),
                                    dbc.Alert("Usuário adicionado!!", id=ids.ALERT_NEW_USER_SUCESS, dismissable=True, is_open=False, style={'margin-top': '20px'}),
                                    dbc.Alert("Preencha os campos com dados válidos!", id=ids.ALERT_NEW_USER_ERROR, color="danger", dismissable=True, is_open=False, style={'margin-top': '20px'})
                                ]),
                            ),
                            table,
                        ],
                    ),
                ),
                # dbc.Col(html.Div("One of three columns")),
            ]
        ),

            className="mt-3"
        )

        tab3_content = dbc.Card(
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardBody(
                        [
                            dbc.Form([name_escritorio, users_input]),
                            dbc.Row(
                                dbc.Col([
                                    dbc.Button("Submit", id=ids.SUBMIT_NEW_ESCRITORIO, n_clicks=0, style={'margin-top': '20px', "justify-content": "center"}),
                                    dbc.Alert("Escritório adicionado!", id=ids.ALERT_NEW_ESCRITORIO_SUCESS, dismissable=True, is_open=False, style={'margin-top': '20px'}),
                                    dbc.Alert("Preencha os campos com dados válidos!", id=ids.ALERT_NEW_ESCRITORIO_ERROR, color="danger", dismissable=True, is_open=False, style={'margin-top': '20px'})
                                ]),
                            ),
                            html.P(self._all_escritorios(), style={'margin-top': '20px'}),

                        ],
                    ),
                ),
                # dbc.Col(html.Div("One of three columns")),
            ]
        ),

            className="mt-3"
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
                        dcc.Tab(
                            tab2_content,
                            id="Control-chart-tab",
                            label="Adicionar Usuários",
                            value="tab2",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            tab3_content,
                            id="add-escritorios",
                            label="Adicionar Escritorio",
                            value="tab3",
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
                html.H1('Config:'),
                html.Hr(),
                # dcc.Markdown(children=markdown_text),
                tabs,

            ], style={'background-color': '#f8f9fa'}
        )
        return home

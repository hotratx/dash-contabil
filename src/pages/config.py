from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import current_user
import dash_bootstrap_components as dbc
from src.handle_pdf import HandlePdf
from src.components.upload import Upload
from src.components import ids, nation_dropdown
from src.database import Crud


markdown_text = f"""
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)

<if this is your first introduction to Markdown!>
"""

handle_pdf = HandlePdf("db")


class PageConfig:
    def __init__(self, app: Dash):
        self._app = app
        self._upload = Upload(app)
        self._crud = Crud()
        self._run()

    def _escritorios(self):
        escs = self._crud.get_escritorios(current_user.get_id())
        self._revert_value_to_label = {}
        i = 0
        for e in escs:
            self._revert_value_to_label[i] = e.name
            i += 1

        return [{'label': es.name, 'value': value} for es, value in zip(escs, range(len(escs)))]

    def _all_escritorios_list(self):
        escs = self._crud.get_escritorios(current_user.get_id())
        resp = []
        for e in escs:
            resp.append(e.name)
        return resp

    def _all_escritorios(self):
        escs = self._crud.get_escritorios(current_user.get_id())
        resp = ''
        for e in escs:
            resp += f'{e.name}, '
        self._all_escs = resp
        return resp

    def _all_users(self, position=0):
        escs = self._crud.get_escritorios(current_user.get_id())
        users = escs[position].users
        resp = ''
        for e in escs:
            for u in e.users:
                resp += f'{u.username} - {e.name} | '
        return resp

    def _run(self):

        @self._app.callback(
            Output(ids.SELECT_ESCRITORIO, "value"),
            Input(ids.SELECT_ALL_NATIONS_BUTTON, "n_clicks"),
        )
        def select_all_nations(n_clicks):
            if n_clicks:
                print(f'DENTRO DO SELECT {self._all_escritorios_list()}')
                return self._all_escritorios_list()


        @self._app.callback(
            Output(ids.SPINNER, "children"),
            Input(ids.HANDLE_PDF_TBN, "n_clicks"),
            State(ids.SELECT_ESCRITORIO, "value"),
        )
        def analise_pdf(n_clicks, value):
            """Callback controle de páginas"""
            value = self._revert_value_to_label[value[0]]
            print(f'VALUE FINAL: {value} - n_clicks: {n_clicks}')
            if n_clicks > 0:
                print('PASSOU DO n_clicks')
                handle_pdf.run(value)
                return "Foi feito o upload dos seguintes arquivos:"
            raise PreventUpdate

        @self._app.callback(
            Output(ids.ALERT_NEW_USER_SUCESS, "is_open"),
            Output(ids.ALERT_NEW_USER_ERROR, "is_open"),
            [Input(ids.SUBMIT_NEW_USER, "n_clicks")],
            [State(ids.NEW_USERNAME, "value"), State(ids.NEW_PASSWORD, "value"), State(ids.SELECT_ESCRITORIO, 'value'), State(ids.ALERT_NEW_USER_SUCESS, 'is_open')],
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
            State(ids.ALERT_NEW_ESCRITORIO_SUCESS, "is_open")
        )
        def add_new_escritorio(n_clicks, value, is_open):
            """Callback controle de páginas"""
            if n_clicks > 0:
                if value:
                    # print(f'VVVVVVVVVVVVVAI ADD NEW ESCRITÓRIO: {value}')
                    e = self._crud.add_escritorio(value, current_user.get_id())
                    print(f'SUCESSO ADD NOVO ESCRIORIO: {e}')
                    self._all_escritorios()
                    return not is_open, is_open
                else:
                    return is_open, not is_open
            return is_open, is_open

    def render(self) -> html.Div:

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

        # escritorio_input = nation_dropdown.render(self._app, self._all_escritorios_list()),
        escritorio_input = dbc.Row(
            [
                dbc.Label("Escritório", html_for="example-password-row", width=2),
                dbc.Col(
                    dbc.Select(
                        id=ids.SELECT_ESCRITORIO,
                        options=self._escritorios(),
                        value=[0]
                    ),
                )
            ],
            className="mb-3",
        )

        table_header = [
            html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
        ]

        row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
        row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
        row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
        row4 = html.Tr([html.Td("Trillian"), html.Td("Asdf")])
                                

        table_body = [html.Tbody([row1, row2, row3, row4])]

        table = dbc.Table(table_header + table_body, bordered=True, style={'margin-top': '20px'})

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
                                    value=self._escritorios()[0]

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
                            html.P(self._all_users(), style={'margin-top': '20px'}),
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
                            dbc.Row(
                                [
                                    dbc.Label("Name", html_for="example-email-row", width=2),
                                    # nation_dropdown.render(self._app, self._all_escritorios_list()),

                                    dbc.Col(
                                        dbc.Input(
                                            type="text", id=ids.NEW_ESCRITORIO, placeholder="Enter nome do escritório"
                                        ),
                                        width=10,
                                    ),
                                ],
                                className="mb-3",
                            ),

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

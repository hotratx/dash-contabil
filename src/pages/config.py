from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import current_user
import dash_bootstrap_components as dbc
from src.handle_pdf import HandlePdf
from src.components.upload import Upload
from src.components import ids
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
        for e in escs:
            self._revert_value_to_label[0] = e.name

        return [{'label': es.name, 'value': 'asdf'} for es in escs]

    def _run(self):
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
            Output(ids.ALERT_NEW_USER, "is_open"),
            [Input(ids.SUBMIT_NEW_USER, "n_clicks")],
            [State(ids.NEW_USERNAME, "value"), State(ids.NEW_PASSWORD, "value"), State(ids.ALERT_NEW_USER, 'is_open')],
        )
        def add_new_user(n_clicks, username, password, is_open):
            """Callback controle de páginas"""
            print(f'USERNAME: {username} - PASSWORD: {password}')
            if n_clicks > 0:
                print('PASSOU DO n_clicks')
                return not is_open
            return is_open
    def render(self) -> html.Div:
        tab1_content = dbc.Card(


            dbc.Row(
                [
                    dbc.Col(html.Div(
                        dbc.CardBody(
                            [
                                html.P(f'Escritorios: {self._escritorios()}', id=ids.OUTPUT_RESULT),
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
                            dbc.Row(
                                [
                                    dbc.Label("Username", html_for="example-email-row", width=2),
                                    dbc.Col(
                                        dbc.Input(
                                            type="username", id=ids.NEW_USERNAME, placeholder="Enter email"
                                        ),
                                        width=10,
                                    ),
                                ],
                                className="mb-3",
                            ),

                            dbc.Row(
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
                            ),
                            dbc.Row(
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
                            ),
                            dbc.Row(
                                dbc.Col([
                                    dbc.Button("Submit", id=ids.SUBMIT_NEW_USER, n_clicks=0, style={'margin-top': '20px', "justify-content": "center"}),
                                    dbc.Alert("Usuário adicionado!!", id=ids.ALERT_NEW_USER, dismissable=True, is_open=False, style={'margin-top': '20px'})
                                ]),
                            )
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
                    ],
                )
            ],
        )


        # tabs = dbc.Tabs(
        #     [
        #         dbc.Tab(tab1_content, label="Novos Dados", tab_style={"margin-left": "35%"}, active_tab_style={"background-color": "#FB79B3"}, active_label_style={"color": "#FB79B3"}),
        #         dbc.Tab(tab2_content, label="Novos Usuários"),
        #         ], style={'background-color': '#f8f9fa'}
        # )

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

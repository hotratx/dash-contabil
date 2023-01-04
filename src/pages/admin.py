from dash import Dash, html, dcc, no_update
import dash_mantine_components as dmc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import current_user
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from src.handle_pdf import HandlePdf
from src.components.upload import Upload
from src.components.dropdown_many import SelectManyA, SelectManyB
from src.components import ids
from src.database import Crud


class PageAdmin:
    def __init__(self, app: Dash):
        self._app = app
        self._crud = Crud()
        self.select_many_a = SelectManyA(app)
        self.select_many_b = SelectManyB(app)
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
            Output(ids.ID_INFO_REMOVE_ESCRITORIO, "hide"),
            Output(ids.ID_ESCRITORIO_WANT_REMOVE, "value"),
            [Input(ids.REMOVE_ESCRITORIO, "n_clicks")],
            [
                State(ids.ID_ESCRITORIO_WANT_REMOVE, "value"),
            ],
            prevent_initial_call=True,
        )
        def remove_escritorio(n_clicks, value):
            if n_clicks > 0:
                self._crud.delete_escritorio(value)
                print(f"\nREMOVER ESCRITORIO: {value}")
                return False

        @self._app.callback(
            Output(ids.ID_INFO_REMOVE_USER, "hide"),
            Output(ids.ID_USER_WANT_REMOVE, "value"),
            [Input(ids.REMOVE_USER, "n_clicks")],
            [
                State(ids.ID_USER_WANT_REMOVE, "value"),
            ],
            prevent_initial_call=True,
        )
        def remove_user(n_clicks, value):
            if n_clicks > 0:
                self._crud.delete_user(value)
                print(f"\nREMOVER USER: {value}")
                return False, ""

        @self._app.callback(
            Output(ids.ALERT_NEW_USER_SUCESS, "is_open"),
            Output(ids.ALERT_NEW_USER_ERROR, "is_open"),
            [Input(ids.SUBMIT_NEW_USER, "n_clicks")],
            [
                State(ids.NEW_USERNAME, "value"),
                State(ids.NEW_PASSWORD, "value"),
                State(ids.SELECT_MANYA, "value"),
                State(ids.ALERT_NEW_USER_SUCESS, "is_open"),
            ],
        )
        def add_new_user(n_clicks, username, password, escritorio, is_open):
            """Callback controle de páginas"""
            if n_clicks > 0:
                if username and password:
                    resp = self._crud.create_user(username, password, escritorio)
                    self._all_users()
                    return not is_open, is_open
                else:
                    return is_open, not is_open
            return is_open, is_open

        @self._app.callback(
            Output(ids.ALERT_NEW_ESCRITORIO_SUCESS, "is_open"),
            Output(ids.ALERT_NEW_ESCRITORIO_ERROR, "is_open"),
            [Input(ids.SUBMIT_NEW_ESCRITORIO, "n_clicks")],
            State(ids.NEW_ESCRITORIO, "value"),
            State(ids.SELECT_MANYB, "value"),
            State(ids.ALERT_NEW_ESCRITORIO_SUCESS, "is_open"),
        )
        def add_new_escritorio(n_clicks, value, users, is_open):
            """Callback controle de páginas"""
            if n_clicks > 0:
                if value:
                    e = self._crud.create_escritorio(value, users)
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
                    dbc.Input(type="text", id=ids.NEW_ESCRITORIO, placeholder="Nome do escritório"),
                    width=10,
                ),
            ],
            className="mb-3",
        )

        users_input = dbc.Row(
            [
                dbc.Label("Usuários", html_for="example-password-row", width=2),
                dbc.Col(self.select_many_b.render(self.get_all_users())),
            ],
            className="mb-3",
        )

        username_input = dbc.Row(
            [
                dbc.Label("Username", html_for="example-text-row", width=2),
                dbc.Col(
                    dbc.Input(type="text", id=ids.NEW_USERNAME, placeholder="Enter username"),
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
                dbc.Col(self.select_many_a.render(self._all_escritorios_list())),
            ],
            className="mb-3",
        )

        # inicio table
        header = [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Usuário"),
                        html.Th("Escritório"),
                    ]
                )
            )
        ]
        rows = [ html.Tr([html.Td(x[0]), html.Td(x[1])]) for x in self._all_users() ]
        body = [html.Tbody(rows)]

        table_content = dmc.Card(
                    id="table11",
                    children=[
                        dmc.CardSection(
                            dmc.Table(
                                header + body,
                                horizontalSpacing=10,
                                striped=True,
                                highlightOnHover=True,
                                withBorder=True,
                                withColumnBorders=True
                            )
                        )
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
        )
        # fim table


        remove_escritorio = dmc.Select(
            label="Select escritório",
            id=ids.ID_ESCRITORIO_WANT_REMOVE,
            placeholder="Select one",
            data=self._all_escritorios_list(),
            searchable=True,
            nothingFound="No options found",
            style={"width": 400, "marginBottom": 10},
        )

        remove_user = dmc.Select(
            label="Select user",
            id=ids.ID_USER_WANT_REMOVE,
            clearable=True,
            placeholder="Select one",
            data=self.get_all_users(),
            searchable=True,
            nothingFound="No options found",
            style={"width": 400, "marginBottom": 10},
        )

        tab3_content = dmc.Card(
                children=[
                    dmc.CardSection(
                        dmc.Center(
                            style={"height": 300, "width": "100%"},
                            children=[
                                dmc.Grid(
                                    children=[
                                        dmc.Col(
                                            dmc.Stack(
                                                [
                                                    remove_escritorio,
                                                    dmc.Button(
                                                        "Remove Escritório",
                                                        id=ids.REMOVE_ESCRITORIO,
                                                        color="red",
                                                        radius="xs",
                                                        leftIcon=DashIconify(icon="clarity:trash-line", width=20),
                                                        style={"width": 200}
                                                    ),
                                                    dmc.Alert(
                                                        title="Escritório removido!",
                                                        id=ids.ID_INFO_REMOVE_ESCRITORIO,
                                                        duration=3000,
                                                        hide=True,
                                                        color="red",
                                                        style={"width": "100%"}
                                                    ),
                                                ],
                                                align="center",
                                                justify="center"
                                            ),
                                        span=6),


                                        dmc.Col(
                                            dmc.Stack(
                                                [
                                                    remove_user,
                                                    dmc.Button(
                                                        "Remove User",
                                                        id=ids.REMOVE_USER,
                                                        n_clicks=0,
                                                        color="red",
                                                        radius="xs",
                                                        leftIcon=DashIconify(icon="clarity:trash-line", width=20),
                                                        style={"width": 200}
                                                    ),
                                                    dmc.Alert(
                                                        title="Usuário removido!",
                                                        id=ids.ID_INFO_REMOVE_USER,
                                                        duration=3000,
                                                        hide=True,
                                                        color="red",
                                                        style={"width": "100%"}
                                                    ),
                                                ],
                                                align="center",
                                                justify="center"
                                            ),
                                        span=6),


                                    ],
                                    gutter="xl",
                                )



                            ],
                        ),


                    ),
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                style={"width": "100%", "margin-top": "200px"},
            )

        tab1_content = dbc.Card(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardBody(
                            [
                                dbc.Form([username_input, password_input, escritorio_input]),
                                dbc.Row(
                                    dbc.Col(
                                        [
                                            dbc.Button(
                                                "Submit",
                                                id=ids.SUBMIT_NEW_USER,
                                                n_clicks=0,
                                                style={"margin-top": "20px", "justify-content": "center"},
                                            ),
                                            dbc.Alert(
                                                "Usuário adicionado!!",
                                                id=ids.ALERT_NEW_USER_SUCESS,
                                                dismissable=True,
                                                is_open=False,
                                                style={"margin-top": "20px"},
                                            ),
                                            dbc.Alert(
                                                "Preencha os campos com dados válidos!",
                                                id=ids.ALERT_NEW_USER_ERROR,
                                                color="danger",
                                                dismissable=True,
                                                is_open=False,
                                                style={"margin-top": "20px"},
                                            ),
                                        ]
                                    ),
                                ),
                            ],
                        ),
                    ),
                ]
            ),
            className="mt-3",
        )

        tab2_content = dbc.Card(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardBody(
                            [
                                dbc.Form([name_escritorio, users_input]),
                                dbc.Row(
                                    dbc.Col(
                                        [
                                            dbc.Button(
                                                "Submit",
                                                id=ids.SUBMIT_NEW_ESCRITORIO,
                                                n_clicks=0,
                                                style={"margin-top": "20px", "justify-content": "center"},
                                            ),
                                            dbc.Alert(
                                                "Escritório adicionado!",
                                                id=ids.ALERT_NEW_ESCRITORIO_SUCESS,
                                                dismissable=True,
                                                is_open=False,
                                                style={"margin-top": "20px"},
                                            ),
                                            dbc.Alert(
                                                "Preencha os campos com dados válidos!",
                                                id=ids.ALERT_NEW_ESCRITORIO_ERROR,
                                                color="danger",
                                                dismissable=True,
                                                is_open=False,
                                                style={"margin-top": "20px"},
                                            ),
                                        ]
                                    ),
                                ),
                            ],
                        ),
                    ),
                    # dbc.Col(html.Div("One of three columns")),
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
                            id="Control-chart-tab",
                            label="Adicionar Usuários",
                            value="tab1",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            tab2_content,
                            id="add-escritorios",
                            label="Adicionar Escritorio",
                            value="tab2",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            tab3_content,
                            id="remover",
                            label="Remover",
                            value="tab3",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                    ],
                ),
            ],
        )

        conttent = dmc.Stack(
            [
                tabs,
                table_content,
            ],
            spacing=60
        )


        home = html.Div(
            className="app-div",
            children=[
                html.H1("Admin:"),
                html.Hr(),
                conttent
                # dcc.Markdown(children=markdown_text),
                # tabs,
                # table_content
            ],
            style={"background-color": "#f8f9fa"},
        )
        return home

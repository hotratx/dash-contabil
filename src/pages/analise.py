from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.plot.plotting import despesas, create_df, pie
from dash.dependencies import Input, Output
from src.components.dropdown import SelectOne
import dash_bootstrap_components as dbc
from src.database import Crud
from flask_login import current_user
from src.components import ids


class PageAnalise:
    def __init__(self, app: Dash):
        self._app = app
        self.select = SelectOne(app)
        self._crud = Crud()
        self.data_escritorios: list = []
        self.data_empresas: list = ['tt', 'asdf']
        self.callback()

    def callback(self):
        self.df = pd.DataFrame()
        @self._app.callback(
            Output(ids.SELECT_EMPRESAS_ANALISE, "options"),
            Input(ids.SELECT_ESCRITORIO_ANALISE, "value"),
        )
        def select_all_options(value):
            empresas = [emp.name for emp in self._crud.get_empresas_from_escritorio(value)]
            self.data_empresas = empresas
            return self.data_empresas

        @self._app.callback(
            Output(ids.DATA_FROM_EMPRESA, "children"),
            Output(ids.FIGURE_ANALISE, "figure"),
            Output(ids.PIE_ANALISE_1, "figure"),
            Output(ids.SELECT_YEAR, "options"),
            Output(ids.SELECT_YEAR, "value"),
            Input(ids.SELECT_EMPRESAS_ANALISE, "value"),
            Input(ids.SELECT_YEAR, "value"),
        )
        def select_data_from_empresa(value, year):
            print(f'VALOR DO VALUE DEVE SER NOME DA EMPRESAS: {value}')
            datas = self._crud.get_datas_from_empresa_name(value)
            try:
                self.df, select_years = create_df(datas)
                if not year:
                    year = select_years[-1]
                fig = despesas(self.df, year)
                fig_pie = pie(self.df, year)
                return datas[0].pis, fig, fig_pie, select_years, year
            except Exception:
                pass

    def _get_escritorios(self):
        if not self.data_escritorios:
            self.data_escritorios = self._crud.get_escritorios_from_user(current_user.get_id())
        return self.data_escritorios

    def escritorios(self):
        if not self.data_escritorios:
            self._get_escritorios()
        return [esc.name for esc in self.data_escritorios]

    def render(self):
        resp = html.Div(
            className="app-div",
            children=[
                dbc.Row(
                    [
                        dbc.Col([
                            html.P("Escritório:"),
                            dcc.Dropdown(
                                id=ids.SELECT_ESCRITORIO_ANALISE,
                                options=[{"label": value, "value": value} for value in self.escritorios()],
                                value=self.escritorios()[0],
                                multi=False,
                            ),

                        ]),
                        dbc.Col([
                            html.P("Empresa:"),
                            dcc.Dropdown(
                                id=ids.SELECT_EMPRESAS_ANALISE,
                                options=[{"label": value, "value": value} for value in self.data_empresas],
                                value=self.data_empresas[0],
                                multi=False,
                            ),
                            html.Span(
                                id=ids.DATA_FROM_EMPRESA,
                                style={"text-align": "center", "margin-top": "10px"},
                            ),
                        ]),
                        dbc.Col([
                            html.P("Ano:"),
                            dcc.Dropdown(
                                id=ids.SELECT_YEAR,
                                multi=False,
                            ),

                        ]),
                    ]
                ),
                dbc.Row([
                    dcc.Graph(
                        id=ids.PIE_ANALISE_1
                    ),
                    dcc.Graph(
                        id=ids.FIGURE_ANALISE,
                        )
                ])
            ]
        )
        return resp

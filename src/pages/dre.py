from dash import Dash, html, dcc
import pandas as pd
from dash.dependencies import Input, Output
from src.components.dropdown import SelectOne
import dash_bootstrap_components as dbc
from src.database import Crud
from flask_login import current_user
from babel.numbers import format_currency
from src.components import ids
from src.components.dre import tab_despesas, tab_impostos, tab_receitas, tab_info

from src.plot import create_df
from src.plot.line import line_lucro
from src.plot.pie import pie, pie_receita_desp, pie_impostos, line_lucro
from src.plot.bar import bar_despesas, bar_receita_bruta, bar_impostos, bar_receitas, bar_receitas_3d


class PageDRE:
    def __init__(self, app: Dash):
        self._app = app
        self.select = SelectOne(app)
        self._crud = Crud()
        self.data_escritorios: list = []
        self.data_empresas: list = ["none", "none"]
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
            # Output("skeleton-graph-container", "children"),
            Output(ids.BAR_DESPESAS, "figure"),
            Output(ids.PIE_ANALISE_1, "figure"),
            Output(ids.BAR_RB, "figure"),
            Output(ids.PIE_IMP, "figure"),
            Output(ids.BAR_RECEITAS, "figure"),
            Output(ids.SELECT_YEAR, "options"),
            Output(ids.SELECT_YEAR, "value"),
            Output(ids.INFO_RECEITA_BRUTA, "children"),
            Output(ids.INFO_DESP_OPE, "children"),
            Output(ids.INFO_IMPOSTOS, "children"),
            Output(ids.INFO_RECEITA_LIQ, "children"),
            Output(ids.INFO_MARG_LUCRO, "children"),
            Input(ids.SELECT_EMPRESAS_ANALISE, "value"),
            Input(ids.SELECT_YEAR, "value"),
        )
        def update_graficos(value, year):
            datas = self._crud.get_datas_from_empresa_name(value)
            try:
                self.df, select_years = create_df(datas)
                if not year:
                    year = select_years[-1]
                if year not in select_years:
                    year = select_years[-1]

                # gráficos
                bar_desp = bar_despesas(self.df, year)
                bar_rb = bar_receita_bruta(self.df, year)
                bar_rec = bar_receitas(self.df, year)
                pie_rece = pie_receita_desp(self.df, year)
                line_l = line_lucro(self.df, year)

                # infos
                df = self.df.loc[str(year)]
                info_receita_bruta = f'{format_currency(df.iloc[0]["rec_bruta_ope"], "BRL", locale="pt_BR")}'
                info_despesa_ope = f'{format_currency(df.iloc[0]["desp_operacionnal"], "BRL", locale="pt_BR")}'
                info_impostos = f'{format_currency(df.iloc[0]["impostos_faturados"], "BRL", locale="pt_BR")}'
                info_receita_liq = f'{format_currency(df.iloc[0]["receita_liquida"], "BRL", locale="pt_BR")}'
                info_marg_lucro = f'{df.iloc[0]["lucro_bruto"]/df.iloc[0]["rec_bruta_ope"]:.2%}'

                return bar_desp, pie_rece, bar_rb, line_l, bar_rec, select_years, year, info_receita_bruta, info_despesa_ope, info_impostos, info_receita_liq, info_marg_lucro
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
        tab1_content = tab_receitas()
        tab2_content = tab_despesas()
        tab3_content = tab_impostos()
        tab4_content = tab_info()

        resp = html.Div(
            id="tabs",
            className="tabs",
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.P("Escritório:"),
                                dcc.Dropdown(
                                    id=ids.SELECT_ESCRITORIO_ANALISE,
                                    options=[{"label": value, "value": value} for value in self.escritorios()],
                                    value=self.escritorios()[0],
                                    multi=False,
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.P("Empresa:"),
                                dcc.Dropdown(
                                    id=ids.SELECT_EMPRESAS_ANALISE,
                                    options=[{"label": value, "value": value} for value in self.data_empresas],
                                    value=self.data_empresas[0],
                                    multi=False,
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.P("Ano:"),
                                dcc.Dropdown(
                                    id=ids.SELECT_YEAR,
                                    multi=False,
                                ),
                            ]
                        ),
                    ],
                ),
                dcc.Tabs(
                    id="app-tabs",
                    value="tab1",
                    className="custom-tabs",
                    style={"margin-top": "30px"},
                    children=[
                        dcc.Tab(
                            tab4_content,
                            id="add-escritorios",
                            label="Lucro",
                            value="tab1",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            tab1_content,
                            id="Specs-tab",
                            label="Receitas",
                            value="tab2",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            tab2_content,
                            id="Control-chart-tab",
                            label="Despesas",
                            value="tab3",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            tab3_content,
                            id="add-escritorios",
                            label="Impostos",
                            value="tab4",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                    ],
                ),
            ],
        )
        return resp

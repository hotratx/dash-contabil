from dash import Dash, html, dcc
import dash_mantine_components as dmc
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
from src.plot.line import line_lucro_liquido, line_despesa, line_margem_lucro
from src.plot.pie import pie, pie_receita_desp, pie_impostos, pie_despesa_info
from src.plot.bar import bar_despesas, bar_receita_bruta, bar_impostos, bar_receitas, bar_receitas_3d, bar_receitas_liquida, bar_perc_custo_x_receita


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
            Output(ids.LINE_DESPESAS, "figure"),
            Output(ids.PIE_ANALISE_1, "figure"),
            Output(ids.BAR_RB, "figure"),
            Output(ids.BAR_RECEITAS, "figure"),
            Output(ids.BAR_IMPOSTOS, "figure"),
            Output(ids.PIE_IMPOSTOS, "figure"),
            Output(ids.BAR_REC_LIQ, "figure"),
            Output(ids.LINE_LUCRO, "figure"),
            Output(ids.LINE_MARGEM_LUCRO, "figure"),
            Output(ids.BAR_PER_CUSTO_X_RECEITA, "figure"),
            # Output(ids.PIE_IMP, "figure"),
            Output(ids.SELECT_YEAR, "data"),
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
                select_years = list(map(str, select_years))
                if not year:
                    year = select_years[-1]
                if year not in select_years:
                    year = select_years[-1]

                # gráficos

                # bar_desp = bar_despesas(self.df, year)
                line_desp = line_despesa(self.df, year)
                bar_rb = bar_receita_bruta(self.df, year)
                bar_rec = bar_receitas(self.df, year)
                bar_imp = bar_impostos(self.df, year)
                pie_imp = pie_impostos(self.df, year)
                pie_rec = pie_despesa_info(self.df, year)
                bar_rec_liq = bar_receitas_liquida(self.df, year)
                line_l = line_lucro_liquido(self.df, year)
                line_ml = line_margem_lucro(self.df, year)
                bar_pcr = bar_perc_custo_x_receita(self.df, year)

                # infos
                df = self.df.loc[str(year)]
                info_receita_bruta = f'{format_currency(df.iloc[0]["rec_bruta_ope"], "BRL", locale="pt_BR")}'
                info_despesa_ope = f'{format_currency(df.iloc[0]["desp_operacional"], "BRL", locale="pt_BR")}'
                info_impostos = f'{format_currency(df.iloc[0]["impostos_faturados"], "BRL", locale="pt_BR")}'
                info_receita_liq = f'{format_currency(df.iloc[0]["receita_liquida"], "BRL", locale="pt_BR")}'
                info_marg_lucro = f'{df.iloc[0]["lucro_bruto"]/df.iloc[0]["rec_bruta_ope"]:.2%}'

                return line_desp, pie_rec, bar_rb, bar_rec, bar_imp, pie_imp, bar_rec_liq, line_l, line_ml, bar_pcr, select_years, year, info_receita_bruta, info_despesa_ope, info_impostos, info_receita_liq, info_marg_lucro
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
        # tab1_content = tab_receitas()
        # tab2_content = tab_despesas()
        # tab3_content = tab_impostos()
        tab4_content = tab_info()

        resp = html.Div(
            id="tabs",
            className="tabs",
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dmc.Select(
                                    id=ids.SELECT_ESCRITORIO_ANALISE,
                                    label="Escritório:",
                                    data=[{"label": value, "value": value} for value in self.escritorios()],
                                    value=self.escritorios()[0],
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                dmc.Select(
                                    id=ids.SELECT_EMPRESAS_ANALISE,
                                    label="Empresa",
                                    data=[{"label": value, "value": value} for value in self.data_empresas],
                                    value=self.data_empresas[0],
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                dmc.Select(
                                    id=ids.SELECT_YEAR,
                                    label="ano"
                                ),
                            ]
                        ),
                    ],
                ),
                dmc.Tabs(
                    id="app-tabs",
                    grow=True,
                    position="center",
                    style={"margin-top": "30px"},
                    children=[
                        dmc.Tab(
                            tab4_content,
                            id="add-escritorios",
                            label="Resumo",
                        ),
                        dmc.Tab(
                            # tab1_content,
                            id="Specs-tab",
                            label="Receitas",
                        ),
                        dmc.Tab(
                            # tab2_content,
                            id="Control-chart-tab",
                            label="Despesas",
                        ),
                        dmc.Tab(
                            # tab3_content,
                            id="add-escritorios",
                            label="Impostos",
                        ),
                    ],
                ),
            ],
        )
        return resp

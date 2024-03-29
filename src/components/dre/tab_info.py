from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from src.components import ids


style1 = {
    "textAlign": "center",
}


def tab_info():
    return html.Div([
        dmc.Grid(
            children=[
                dmc.Col(
                    dbc.Card([
                        dmc.Col(html.Div([
                            dmc.Badge("Receita Bruta", size="md", radius="xs", fullWidth=True),
                            dmc.Text(id=ids.INFO_RECEITA_BRUTA, weight=500, style={"margin-top": "7px"}),
                            ]), style=style1)
                    ]), span=2
                ),

                dmc.Col(
                    dbc.Card([
                        dmc.Col(html.Div([
                            dmc.Badge("Desp. Oper.", size="md", color="yellow", radius="xs", fullWidth=True),
                            dmc.Text(id=ids.INFO_DESP_OPE, weight=500, style={"margin-top": "7px"})
                        ]), style=style1)
                    ]), span=2
                ),


                dmc.Col(
                    dbc.Card([
                        dmc.Col(html.Div([
                            dmc.Badge("Impostos", size="md", color="red", radius="xs", fullWidth=True),
                            dmc.Text(id=ids.INFO_IMPOSTOS, weight=500, style={"margin-top": "7px"})
                        ]), style=style1)
                    ]), span=2
                ),


                dmc.Col(
                    dbc.Card([
                        dmc.Col(html.Div([
                            dmc.Badge("Rec. Líquida", size="md", color="green", radius="xs", fullWidth=True),
                            dmc.Text(id=ids.INFO_RECEITA_LIQ, weight=500, style={"margin-top": "7px"})
                        ]), style=style1)
                    ]), span=2
                ),

                dmc.Col(
                    dbc.Card([
                        dmc.Col(html.Div([
                            dmc.Badge("Mar. de Lucro", size="md", color="violet", radius="xs", fullWidth=True),
                            dmc.Text(id=ids.INFO_MARG_LUCRO, weight=500, style={"margin-top": "7px"})
                        ]), style=style1)
                    ]), span=2
                ),
            ],
            gutter="xl", justify="space-between"
        ),

        dmc.Grid(
            children=[
                dmc.Col(
                    dbc.Card([
                        dbc.CardBody(
                            dmc.Col(html.Div([
                                # dmc.Text("Aqui temos a receita bruta:", weight=500, style={"margin-top": "7px"}),

                                dbc.Row([
                                    dbc.Col([
                                        dmc.Skeleton(
                                            visible=False,
                                            children=dcc.Graph(id=ids.BAR_RB)
                                        ),
                                    ]),


                                    dbc.Col([
                                        dmc.Skeleton(
                                            visible=False,
                                            children=dcc.Graph(id=ids.BAR_RECEITAS)
                                        ),
                                    ]),
                                ]),
                            ]))
                        ),
                    ]), span=12
                ),


                dmc.Col(
                    dbc.Card([
                        dbc.CardBody(
                            dmc.Col(html.Div([
                                # dmc.Text("Aqui temos as despesas:", weight=500, style={"margin-top": "7px"}),

                                dbc.Row([
                                    dbc.Col([
                                        dmc.Skeleton(
                                            visible=False,
                                            children=dcc.Graph(id=ids.LINE_DESPESAS)
                                        ),
                                    ]),


                                    dbc.Col([
                                        dmc.Skeleton(
                                            visible=False,
                                            children=dcc.Graph(id=ids.PIE_ANALISE_1)
                                        ),
                                    ]),
                                ]),
                            ]))
                        ),
                    ]), span=12
                ),

                dmc.Col(
                    dbc.Card([
                        dbc.CardBody(
                            dmc.Col(html.Div([
                                # dmc.Text("Aqui temos os Impostos:", weight=500, style={"margin-top": "7px"}),
                                dbc.Row([
                                    dbc.Col(
                                        dmc.Skeleton(
                                            visible=False,
                                            children=dcc.Graph(id=ids.BAR_IMPOSTOS)
                                        ),
                                    ),

                                    dbc.Col([
                                        dmc.Skeleton(
                                            visible=False,
                                            children=dcc.Graph(id=ids.PIE_IMPOSTOS)
                                        ),
                                    ]),
                                ]),
                            ]))
                        ),
                    ]), span=12
                ),



                dmc.Col(
                    dbc.Card([
                        dbc.CardBody(
                            dmc.Col(html.Div([
                                # dmc.Text("Receita Líquida", weight=500, style={"margin-top": "7px"}),
                                dbc.Row([
                                    dbc.Col(
                                        dmc.Skeleton(
                                            visible=False,
                                            children=dcc.Graph(id=ids.BAR_REC_LIQ)
                                        ),
                                    ),

                                    dbc.Col([
                                        dmc.Skeleton(
                                            visible=False,
                                            children=dcc.Graph(id=ids.LINE_LUCRO)
                                        ),
                                    ]),
                                ]),
                            ]))
                        ),
                    ]), span=12
                ),


                dmc.Col(
                    dbc.Card([
                        dbc.CardBody(
                            dmc.Col(html.Div([
                                # dmc.Text("Margem de Lucro Bruto", weight=500, style={"margin-top": "7px"}),
                                dbc.Row([
                                    dbc.Col(
                                        dmc.Skeleton(
                                            visible=False,
                                            children=dcc.Graph(id=ids.LINE_MARGEM_LUCRO)
                                        ),
                                    ),

                                    dbc.Col(
                                        dmc.Skeleton(
                                            visible=False,
                                            children=dcc.Graph(id=ids.BAR_PER_CUSTO_X_RECEITA)
                                        ),
                                    ),
                                ]),
                            ]))
                        ),
                    ]), span=12
                ),


            ],
            gutter="xl", justify="space-around"
        ),
    ])

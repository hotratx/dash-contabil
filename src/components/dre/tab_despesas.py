from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from src.components import ids


def tab_despesas():
    return dbc.Card(
        [
            # dbc.Row(
            #     dbc.Col(
            #         dcc.Graph(
            #             id=ids.BAR_DESPESAS,
            #         )
            #     )
            # ),
            # dbc.Row(
            #     dbc.Col(
            #         [
            #             dcc.Graph(id=ids.PIE_ANALISE_1),
            #         ]
            #     ),
            # ),
        ]
    )


style = {
    "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
    "textAlign": "center",
}
style1 = {
    "textAlign": "center",
}


def tab_impostos():
    return html.Div(
        dbc.Row(
            dbc.Col([
                dcc.Graph(id=ids.PIE_IMP),
            ]),
        )
    )


def tab_receitas():
    return dbc.Card(
            [
                # dbc.Row(
                #     dbc.Col(
                #         [
                #             dcc.Graph(id=ids.BAR_RB),
                #         ]
                #     ),
                # ),
                dbc.Row(
                    dbc.Col(
                        [
                            dcc.Graph(id=ids.PIE_IMP),
                        ]
                    ),
                ),
            ]
        )

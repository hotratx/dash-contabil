from dash import dcc
import dash_bootstrap_components as dbc
from src.components import ids


def tab_despesas():
    return dbc.Card(
        [
            dbc.Row(
                dbc.Col(
                    dcc.Graph(
                        id=ids.BAR_DESPESAS,
                    )
                )
            ),
            dbc.Row(
                dbc.Col(
                    [
                        dcc.Graph(id=ids.PIE_ANALISE_1),
                    ]
                ),
            ),
        ]
    )


def tab_impostos():
    return dbc.Card(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                dcc.Graph(id=ids.PIE_IMP),
                            ]
                        ),
                    )
                ]
            )


def tab_receitas():
    return dbc.Card(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            dcc.Graph(id=ids.BAR_RB),
                        ]
                    ),
                ),
                dbc.Row(
                    dbc.Col(
                        [
                            dcc.Graph(id=ids.BAR_RECEITAS),
                        ]
                    ),
                ),
            ]
        )

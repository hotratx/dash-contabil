import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
from datetime import datetime


funct_dates = lambda x: x.strftime("%d-%m-%Y")


def line_lucro_liquido(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    values = df["result_liquido_exer"].values / df["rec_bruta_ope"].values * 100
    values = values.round(decimals=2)
    fig = go.Figure(
        data=[
            go.Line(name="Margem de lucro líquido", x=funct_dates(df.index).values, y=values),
        ]
    )
    # fig.update_traces(hole=.4, hoverinfo="label+value+name")
    fig.update_layout(yaxis_ticksuffix="%", barmode="stack", title="Margem de lucro líquido", width=500, height=400)
    return fig


def line_despesa(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    values = df["desp_operacional"].values
    fig = go.Figure(
        data=[
            go.Line(name="Desp. Operacional", x=funct_dates(df.index).values, y=values),
        ]
    )
    # fig.update_traces(hole=.4, hoverinfo="label+value+name")
    fig.update_layout(barmode="stack", title="Despesas Operacionais", width=500, height=400)
    return fig


def line_margem_lucro(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    values = df["lucro_bruto"].values / df["rec_bruta_ope"].values * 100
    values = values.round(decimals=2)
    fig = go.Figure(
        data=[
            go.Line(name="Margem de lucro", x=funct_dates(df.index).values, y=values),
        ]
    )
    # fig.update_traces(hole=.4, hoverinfo="label+value+name")
    fig.update_layout(yaxis_ticksuffix="%", barmode="stack", title="Margem de lucro", width=500, height=400)
    return fig

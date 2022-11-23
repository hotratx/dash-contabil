import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd


funct_dates = lambda x: x.strftime("%d-%m-%Y")


def bar_receita_bruta(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    fig = go.Figure(
        data=[
            go.Bar(name="Receita Bruta", x=funct_dates(df.index).values, y=df["rec_bruta_ope"].values),
            go.Bar(
                name="Custo Mercadorias Revendidas",
                x=funct_dates(df.index).values,
                y=df["custo_mercadorias_revendidas"].values,
            ),
        ]
    )
    fig.update_layout(barmode="stack", title="Receita Bruta Operacional x Custo Mercadorias Revendidas")
    return fig


def bar_impostos(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    fig = go.Figure(
        data=[
            go.Bar(name="ICMS", x=funct_dates(df.index).values, y=df["icms"].values),
            go.Bar(name="CONFINS", x=funct_dates(df.index).values, y=df["confins"].values),
        ]
    )
    fig.update_layout(barmode="stack", title="Impostos")
    return fig


def bar_receitas(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    fig = go.Figure(
        data=[
            go.Bar(name="Rec. Liq.", x=funct_dates(df.index).values, y=df["receita_liquida"].values),
            go.Bar(name="Rec. Fin.", x=funct_dates(df.index).values, y=df["receitas_financeiras"].values),
        ]
    )
    fig.update_layout(barmode="stack", title="Receita Líquida", width=500, height=500)
    return fig


def bar_despesas(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    fig = go.Figure(
        data=[
            go.Bar(name="Desp Adm.", x=funct_dates(df.index).values, y=df["desp_admin"].values),
            go.Bar(name="Desp Oper.", x=funct_dates(df.index).values, y=df["desp_operacionnal"].values),
            go.Bar(name="Desp Trib.", x=funct_dates(df.index).values, y=df["desp_trib"].values),
            go.Bar(name="Desp Fin.", x=funct_dates(df.index).values, y=df["desp_financeiras"].values),
        ]
    )
    fig.update_layout(barmode="stack", title="Despesas por trimestre")
    return fig



def bar_receitas_3d(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    z = df["receita_liquida"].values
      
    fig = go.Figure(data=[go.Mesh3d(
      x=funct_dates(df.index).values, y=df["receita_liquida"].values, z=z, color='green', opacity=0.20)])
      



    # fig = go.Figure(
    #     data=[
    #         go.Bar(name="Rec. Liq.", x=funct_dates(df.index).values, y=df["receita_liquida"].values),
    #         go.Bar(name="Rec. Fin.", x=funct_dates(df.index).values, y=df["receitas_financeiras"].values),
    #     ]
    # )
    # fig.update_layout(barmode="stack", title="Receita Líquida")
    return fig



import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime


funct_dates = lambda x: x.strftime("%d-%m-%Y")


def create_df(datas: list):
    df = pd.DataFrame()
    for data in datas:
        df0 = pd.DataFrame(data.dict(), index=[0])
        df0.set_index('tri', inplace=True)
        df = pd.concat([df, df0])
    return df, list(set(df.index.year.values))


def despesas(df: pd.DataFrame, year):
    # fig = px.bar(x=funct_dates(df.index).values, y=[df["desp_admin"], df["desp_operacionnal"], df["desp_trib"]], title="Despesas",  text_auto=True, height=500)
    print(f'RECEBENDO YEAR XXXXXXXXXXXXXXXXXXXXX {year}')
    df = df.loc[str(year)]
    fig = go.Figure(data=[
        go.Bar(name='Desp Admin', x=funct_dates(df.index).values, y=df["desp_admin"].values),
        go.Bar(name='Desp Opera', x=funct_dates(df.index).values, y=df["desp_operacionnal"].values),
        go.Bar(name='Desp Trib', x=funct_dates(df.index).values, y=df["desp_trib"].values)
    ])
    fig.update_layout(barmode='stack', title="Despesas")
    return fig


def pie(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    fig = go.Figure(data=[
        go.Pie(name='Desp Admin', values=df["desp_admin"].values),
    ])
    return fig


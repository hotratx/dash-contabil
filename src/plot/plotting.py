import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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


def pie(df: pd.DataFrame, year, tri):
    df = df.loc[str(year)]
    fig = go.Figure(data=[
        go.Pie(name='Desp Admin', values=[df.iloc[tri]["desp_admin"], df.iloc[tri]["rec_bruta_ope"]]),
    ])
    fig.update_layout(title="Despesas", height=400)
    return fig


def pie_new(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    labels = ['Desp. Admin', 'Receita Bruta']
    fig = make_subplots(rows=1, cols=4, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=[df.iloc[0]["desp_admin"], df.iloc[0]["rec_bruta_ope"]], name="1 tri"),
                  1, 1)
    fig.add_trace(go.Pie(labels=labels, values=[df.iloc[1]["desp_admin"], df.iloc[1]["rec_bruta_ope"]], name="2 tri"),
                  1, 2)
    fig.add_trace(go.Pie(labels=labels, values=[df.iloc[2]["desp_admin"], df.iloc[2]["rec_bruta_ope"]], name="3 tri"),
                  1, 3)
    fig.add_trace(go.Pie(labels=labels, values=[df.iloc[3]["desp_admin"], df.iloc[3]["rec_bruta_ope"]], name="4 tri"),
                  1, 4)

# Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text=f"Receita Bruta x Despesas Admin {year}",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='1T', x=0.09, y=0.5, font_size=20, showarrow=False),
                     dict(text='2T', x=0.37, y=0.5, font_size=20, showarrow=False),
                     dict(text='3T', x=0.63, y=0.5, font_size=20, showarrow=False),
                     dict(text='4T', x=0.91, y=0.5, font_size=20, showarrow=False)
        ]
    )
    return fig

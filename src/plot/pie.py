import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
from datetime import datetime


funct_dates = lambda x: x.strftime("%d-%m-%Y")


def pie(df: pd.DataFrame, year, tri):
    df = df.loc[str(year)]
    fig = go.Figure(
        data=[
            go.Pie(name="Desp Admin", values=[df.iloc[tri]["desp_admin"], df.iloc[tri]["rec_bruta_ope"]]),
        ]
    )
    fig.update_layout(title="Despesas", width=500, height=400)
    return fig


def pie_despesa_info(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    labels = ["Desp. Oper.", "Receita Bruta"]
    fig = go.Figure(
        data=[
            go.Pie(labels=labels, values=[df.iloc[0]["desp_operacional"], df.iloc[0]["rec_bruta_ope"]]),
        ]
    )
    fig.update_layout(title="Despesa Operacional x Receita Bruta", width=500, height=400)
    return fig


def pie_impostos(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    labels = ["ICMS", "COFINS", "PIS", "IR", "CSSL"]
    fig = go.Figure(
        data=[
            go.Pie(labels=labels, values=[
                df.iloc[0]["icms"],
                df.iloc[0]["cofins"],
                df.iloc[0]["pis"],
                df.iloc[0]["contri_social_sobre_lucro"],
                df.iloc[0]["imposto_renda"]
            ])
        ]
    )
    fig.update_layout(title="Impostos", width=500, height=400)
    return fig


def pie_receita_desp(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    labels = ["Desp. Oper.", "Receita Bruta"]
    fig = make_subplots(
        rows=1, cols=4, specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}, {"type": "domain"}]]
    )
    fig.add_trace(
        go.Pie(labels=labels, values=[df.iloc[0]["desp_operacional"], df.iloc[0]["rec_bruta_ope"]], name="1 tri"), 1, 1
    )
    fig.add_trace(
        go.Pie(labels=labels, values=[df.iloc[1]["desp_operacional"], df.iloc[1]["rec_bruta_ope"]], name="2 tri"), 1, 2
    )
    fig.add_trace(
        go.Pie(labels=labels, values=[df.iloc[2]["desp_operacional"], df.iloc[2]["rec_bruta_ope"]], name="3 tri"), 1, 3
    )
    fig.add_trace(
        go.Pie(labels=labels, values=[df.iloc[3]["desp_operacional"], df.iloc[3]["rec_bruta_ope"]], name="4 tri"), 1, 4
    )

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=0.4, hoverinfo="label+value+percent+name")

    fig.update_layout(
        title_text=f"Receita Bruta x Despesas Operacional {year}",
        # Add annotations in the center of the donut pies.
        annotations=[
            dict(text="1T", x=0.09, y=0.5, font_size=20, showarrow=False),
            dict(text="2T", x=0.37, y=0.5, font_size=20, showarrow=False),
            dict(text="3T", x=0.63, y=0.5, font_size=20, showarrow=False),
            dict(text="4T", x=0.91, y=0.5, font_size=20, showarrow=False),
        ], width=500, height=400
    )
    return fig


def pie_impostos_four(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    labels = ["ICMS", "CONFINS", "PIS", "CSSL"]
    fig = make_subplots(
        rows=1, cols=4, specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}, {"type": "domain"}]]
    )
    fig.add_trace(
        go.Pie(
            labels=labels,
            values=[
                df.iloc[0]["icms"],
                df.iloc[0]["cofins"],
                df.iloc[0]["pis"],
                df.iloc[0]["contri_social_sobre_lucro"],
            ],
            name="1 tri",
        ),
        1,
        1,
    )
    fig.add_trace(
        go.Pie(
            labels=labels,
            values=[
                df.iloc[1]["icms"],
                df.iloc[1]["cofins"],
                df.iloc[1]["pis"],
                df.iloc[1]["contri_social_sobre_lucro"],
            ],
            name="2 tri",
        ),
        1,
        2,
    )
    fig.add_trace(
        go.Pie(
            labels=labels,
            values=[
                df.iloc[2]["icms"],
                df.iloc[2]["cofins"],
                df.iloc[2]["pis"],
                df.iloc[2]["contri_social_sobre_lucro"],
            ],
            name="3 tri",
        ),
        1,
        3,
    )
    fig.add_trace(
        go.Pie(
            labels=labels,
            values=[
                df.iloc[3]["icms"],
                df.iloc[3]["cofins"],
                df.iloc[3]["pis"],
                df.iloc[3]["contri_social_sobre_lucro"],
            ],
            name="4 tri",
        ),
        1,
        4,
    )

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=0.4, hoverinfo="label+value+percent+name")

    fig.update_layout(
        title_text=f"Impostos {year}",
        # Add annotations in the center of the donut pies.
        annotations=[
            dict(text="1T", x=0.09, y=0.5, font_size=20, showarrow=False),
            dict(text="2T", x=0.37, y=0.5, font_size=20, showarrow=False),
            dict(text="3T", x=0.63, y=0.5, font_size=20, showarrow=False),
            dict(text="4T", x=0.91, y=0.5, font_size=20, showarrow=False),
        ], width=500, height=400
    )
    return fig


def line_lucro(df: pd.DataFrame, year):
    df = df.loc[str(year)]
    values = df["result_liquido_exer"].values / df["rec_bruta_ope"].values
    fig = go.Figure(
        data=[
            go.Line(name="Margem de lucro líquido", x=funct_dates(df.index).values, y=values),
        ]
    )
    # fig.update_traces(hole=.4, hoverinfo="label+value+name")
    fig.update_layout(barmode="stack", title="Margem de lucro líquido", width=500, height=400)
    return fig

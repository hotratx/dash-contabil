import pandas as pd
from math import pi

import plotly.express as px


def plot(data: pd.DataFrame):
    fig = px.pie(data, values='values', names='tipo')
    return fig

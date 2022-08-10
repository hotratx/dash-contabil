from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc




def render() -> dbc.Card:
    CARD_STYLE = {
            'width': '300px',
            'min-height': '300px',
            'padding-right': '25px',
            'padding-top': '25px',
            'padding-left': '25px',
            'align-self': 'center',
    }
    login = dbc.Card([
        html.Legend("Login", style={'padding-top': '20px'}),
        dbc.Input(id="user_login", placeholder="Username", type="text", style={'margin-top': '10px'}),
        dbc.Input(id="pwd_login", placeholder="Password", type="password", style={'margin-top': '10px'}),
        dbc.Button("Login", id="login_btn", style={'margin-top': '10px'}),
        html.Span("", style={"text-align": "center", 'margin-top': '10px'}),
    ], style=CARD_STYLE)
    return login

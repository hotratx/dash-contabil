from dash import html, dcc
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
        dcc.Location(id='url_login', refresh=True),
        html.Legend("Login", style={'padding-top': '20px'}),
        dbc.Input(id="user-login", placeholder="Username", type="text", style={'margin-top': '10px'}),
        dbc.Input(id="pwd-login", placeholder="Password", type="password", style={'margin-top': '10px'}),
        dbc.Button("Login", n_clicks=0, id="login-btn", style={'margin-top': '10px'}),
        html.Span(id="output-state", style={"text-align": "center", 'margin-top': '10px'}),
        html.Br(),
    ], style=CARD_STYLE)
    return login

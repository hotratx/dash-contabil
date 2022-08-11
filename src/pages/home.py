from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from flask_login import logout_user, current_user
from src.components import nation_dropdown


markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)

<if this is your first introduction to Markdown!>
'''


def render(app: Dash) -> html.Div:
    CARD_STYLE = {
            'width': '300px',
            'min-height': '300px',
            'padding-right': '25px',
            'padding-top': '25px',
            'padding-left': '25px',
            'align-self': 'center',
    }


    home = html.Div(
        className="app-div",
        children=[
            dcc.Location(id='url_logout', refresh=True),
            html.H1(app.title),
            html.Hr(),
            dbc.Button("Logout", id="logout-btn", n_clicks=0, color="dark"),
            dcc.Markdown(children=markdown_text)
        ])
    return home

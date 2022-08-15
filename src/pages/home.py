from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from flask_login import logout_user, current_user
from src.components import nation_dropdown



markdown_text = """
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)

<if this is your first introduction to Markdown!>
"""


def render(app: Dash) -> html.Div:
    home = html.Div(
        className="app-div",
        children=[
            dcc.Location(id="url_logout", refresh=True),
            html.H1(app.title),
            html.Hr(),
            dbc.Button("Logout", id="logout-btn", n_clicks=0, color="dark"),
            dcc.Markdown(children=markdown_text),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '30%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.P(id='output-result-1'),
            html.Div(id='output-data-upload'),
            dbc.Button("Analisar pdf", id="handle-pdf", n_clicks=0, color="dark"),
            html.P(id="dummy"),
        ],
    )
    return home



import base64
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from flask_login import logout_user, current_user
from src.components import nation_dropdown
from src.handle_pdf import HandlePdf



markdown_text = """
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)

<if this is your first introduction to Markdown!>
"""

handle_pdf = HandlePdf('db')

def render(app: Dash) -> html.Div:
    @app.callback(
        Output('dummy', 'children'),
        [Input("handle-pdf", "n_clicks")],
    )
    def analise_pdf(n_clicks):
        """Callback controle de páginas"""
        if n_clicks > 0:
            handle_pdf.run()
            print('HANDLE PDF -----')


    @app.callback(Output('output-data-upload', 'children'),
              Output('output-result', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
                  State('upload-data', 'last_modified'))
    def update_output(list_of_contents, list_of_names, list_of_dates):
        print(f'list_of_names: {list_of_names}, list_of_dates: {list_of_dates}')
        if list_of_names is not None:
            resp = []
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
                content = parse_contents(c, n, d)
                if content:
                    resp.append(html.P(n))
            response = html.Span(resp)
            if resp:
                return response, 'Foi feito o upload dos arquivos:'
            return '', 'O upload é feito apenas para arquivos .pdf'

        raise PreventUpdate

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
            html.P(id='output-result'),
            html.Div(id='output-data-upload'),
            dbc.Button("Analisar pdf", id="handle-pdf", n_clicks=0, color="dark"),
            html.P(id="dummy"),
        ],
    )
    return home


def parse_contents(contents, filename, date):
    print(f'entrou no parse_contents filename: {filename}\ntipo: {type(contents)}')
    # content_type, content_string = contents.split(',')

    try:
        if 'pdf' in filename:
            data = contents.encode("utf8").split(b";base64,")[1]
            with open(f'pdfs/{filename}', "wb") as fp:
                fp.write(base64.decodebytes(data))
            return True
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

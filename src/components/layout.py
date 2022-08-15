import base64
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from flask_login import login_user, UserMixin, logout_user, current_user
from src.pages import home, login
from src.database.crud import CRUDUser
from src.password import get_password_hash, verify_password
from src.handle_pdf import HandlePdf

handle_pdf = HandlePdf('db')


class User(UserMixin):
    def __init__(self, username):
        self.id = username


def create_layout(app: Dash) -> dbc.Container:


    @app.callback(
        Output('dummy', 'children'),
        [Input("handle-pdf", "n_clicks")],
    )
    def analise_pdf(n_clicks):
        """Callback controle de páginas"""
        if n_clicks > 0:
            handle_pdf.run()
            print('HANDLE PDF -----')
        raise PreventUpdate


    @app.callback(Output('output-data-upload', 'children'),
              Output('output-result-1', 'children'),
              [Input('upload-data', 'contents')],
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


    @app.callback(
        Output("url_login", "pathname"),
        Output("output-state", "children"),
        [Input("login-btn", "n_clicks")],
        [State("user-login", "value"), State("pwd-login", "value")],
    )
    def login_button_click(n_clicks, username, password):
        """Callback do component Login"""
        if n_clicks > 0:
            u = CRUDUser()
            user_model = u.get(username)
            if user_model and password:
                hash = verify_password(password, user_model.password)
                user = User(user_model.username)
                if hash:
                    login_user(user)
                    return ("/home", "")

            return ("/login", "Incorrect username or password")
        raise PreventUpdate

    @app.callback(
        Output("url_logout", "pathname"), Input("logout-btn", "n_clicks")
    )
    def logout_button_click(n_clicks):
        """Callback controle de páginas"""
        if n_clicks > 0:
            return "/logout"

    @app.callback(
        Output("page-content", "children"),
        Input("base-url", "pathname"),
    )
    def render_page_content(pathname):
        """Callback controle de páginas"""
        if pathname == "/login" or pathname == "/":
            return login.render()
        elif pathname == "/home":
            if current_user.is_authenticated:
                return home.render(app)
            else:
                return login.render()
        elif pathname == "/logout":
            print("ENTROU NO LOGOUT")
            if current_user.is_authenticated:
                logout_user()
                return login.render()

    main = dbc.Container(
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Location(id="base-url", refresh=False),
                            html.Div(
                                id="page-content",
                                style={
                                    "height": "100vh",
                                    "display": "flex",
                                    "justify-content": "center",
                                },
                            ),
                        ]
                    )
                ]
            ),
        ],
        fluid=True,
    )

    return main



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

import base64
from dash import Dash, html, dcc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from . import ids


class Upload:
    def __init__(self, app: Dash):
        self._app = app
        self._run()

    def _run(self):
        @self._app.callback(
            Output(ids.OUTPUT_DATA_UPLOAD, "children"),
            [Input(ids.UPLOAD_DATA, "contents")],
            State(ids.UPLOAD_DATA, "filename"),
            State(ids.UPLOAD_DATA, "last_modified"),
        )
        def update_output(list_of_contents, list_of_names, list_of_dates):
            if list_of_names is not None:
                resp = []
                for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
                    content = parse_contents(c, n, d)
                    if content:
                        resp.append(html.P(n))
                response = html.Span(resp)
                if resp:
                    return response, "Foi feito o upload dos arquivos:"
                return "", "O upload é feito apenas para arquivos .pdf"
            raise PreventUpdate

    def render(self) -> dcc.Upload:
        return dcc.Upload(
            id=ids.UPLOAD_DATA,
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        )


def parse_contents(contents, filename, date):
    try:
        if "pdf" in filename:
            data = contents.encode("utf8").split(b";base64,")[1]
            with open(f"pdfs/{filename}", "wb") as fp:
                fp.write(base64.decodebytes(data))
            return True
    except Exception as e:
        print(f'Parse contents error: {e}')
        return html.Div(["There was an error processing this file."])

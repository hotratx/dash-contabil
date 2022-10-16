from dash import Dash, html, dcc
from src.plot.plotting import fig



class PageAnalise:
    def __init__(self, app: Dash):
        self._app = app

    def _run(self):
        pass

    def render(self) -> dcc.Graph:
        return dcc.Graph(
            id='example-graph',
            figure=fig
        )
        # return html.P("This is the content of page 1!")

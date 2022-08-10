from dash import Dash, html
import dash_bootstrap_components as dbc
from src.components.layout import create_layout

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def main() -> None:
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "Medal dashboard"
    app.layout = create_layout(app)
    app.run()


if __name__ == "__main__":
    main()

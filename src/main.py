from flask import Flask
from flask_login import LoginManager, UserMixin
from dash import Dash
import dash_bootstrap_components as dbc
from src.components.layout import create_layout
from src.database import Crud

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)

app = Dash(
    __name__,
    server=server,
    title="Example Dash login",
    update_title="Loading...",
    external_stylesheets=[dbc.themes.PULSE],
    suppress_callback_exceptions=True,
)

server.config.update(SECRET_KEY="ASDKFJASDOIFJKLJRFASDFASDF")

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


class User(UserMixin):
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """Pega o username salvo no cookie"""
    u = Crud()
    user_model = u.get_user(username)
    if not user_model:
        return
    user = User(user_model.username)
    return user


def main() -> None:
    app.title = "Contábil"
    app.layout = create_layout(app)
    app.run_server(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    main()

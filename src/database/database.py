import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

load_dotenv()

# db_host = os.environ.get("POSTGRES_HOST")
# db_name = os.environ.get("POSTGRES_NAME")
# db_password = os.environ.get("POSTGRES_PASSWORD")
# db_user = os.environ.get("POSTGRES_USER")

# print(f'nomes do env: name: {db_name}, host: {db_host}, password: {db_password}, user: {db_user}')

sqlite_file_name = "db_dash.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


# def create_db():
# SQLModel.metadata.drop_all(engine)
# SQLModel.metadata.create_all(engine)

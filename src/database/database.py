from sqlmodel import create_engine
from src import settings

DB_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_hostname}:{settings.postgres_port}/{settings.postgres_db}"

engine = create_engine(DB_URL, echo=True)

# sqlite_file_name = "db_dash.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"

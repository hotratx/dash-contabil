from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_hostname: str
    postgres_db: str
    postgres_password: str
    postgres_user: str
    postgres_port: str

    class Config:
        env_file = ".env"

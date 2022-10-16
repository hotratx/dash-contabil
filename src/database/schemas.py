from typing import Optional
from sqlmodel import SQLModel


class IEscritorio(SQLModel):
    name: str
    user: list
    empresas: list


class IUser(SQLModel):
    username: str
    password: list
    escritorios: list


class IEmpresa(SQLModel):
    name: str
    ie: str
    cnpj: str
    escritorio: IEscritorio
    datas: "IEmpresa"


class IDataDre(SQLModel):
    rbo: str
    empresa: IEmpresa

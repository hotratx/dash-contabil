from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class UserEscritorioLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    escritorio_id: Optional[int] = Field(
        default=None, foreign_key="escritorio.id", primary_key=True
    )


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    escritorios: List["Escritorio"] = Relationship(back_populates="users", link_model=UserEscritorioLink)


class Escritorio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    users: List[User] = Relationship(back_populates="escritorios", link_model=UserEscritorioLink)
    empresas: List["Empresa"] = Relationship(back_populates="escritorio")


class Empresa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    ie: str
    cnpj: str
    escritorio_id: Optional[int] = Field(default=None, foreign_key="escritorio.id")
    escritorio: Optional["Escritorio"] = Relationship(back_populates="empresas")
    datas: List["DataDre"] = Relationship(back_populates="empresa")


class DataDre(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    rbo: Optional[str] = Field(default=None)
    empresa_id: Optional[int] = Field(default=None, foreign_key="empresa.id")
    empresa: Optional[Escritorio] = Relationship(back_populates="datas")

from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from .database import engine


class UserEscritorioLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    escritorio_id: Optional[int] = Field(default=None, foreign_key="escritorio.id", primary_key=True)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    escritorios: List["Escritorio"] = Relationship(back_populates="users", link_model=UserEscritorioLink)


class Escritorio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    users: List[User] = Relationship(back_populates="escritorios", link_model=UserEscritorioLink)
    empresas: List["Empresa"] = Relationship(back_populates="escritorio")


class Empresa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    cnpj: str
    escritorio_id: Optional[int] = Field(default=None, foreign_key="escritorio.id")
    escritorio: Optional["Escritorio"] = Relationship(back_populates="empresas")
    dados: List["Dadosdre"] = Relationship(back_populates="empresa")


class Dadosdre(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tri: datetime = Field(default=None)
    rec_bruta_ope: Optional[float] = Field(default=None)
    fatu_pro_merc_serv: Optional[float]
    vendas_mercadorias: Optional[float]
    dedu_receita: Optional[float]
    impostos_faturados: Optional[float]
    icms: Optional[float]
    cofins: Optional[float]
    pis: Optional[float]
    outras_deducoes: Optional[float]
    vendas_can_dev: Optional[float]
    receita_liquida: Optional[float]
    custo_mercad_ser_pro_vendidos: Optional[float]
    custo_mercadorias_revendidas: Optional[float]
    lucro_bruto: Optional[float]
    desp_operacionnal: Optional[float]
    desp_admin: Optional[float]
    desp_trib: Optional[float]
    resultado_financeiro: Optional[float]
    receitas_financeiras: Optional[float]
    desp_financeiras: Optional[float]
    res_antes_das_part: Optional[float]
    res_antes_imp_renda: Optional[float]
    contri_social_sobre_lucro: Optional[float]
    importo_renda: Optional[float]
    result_liquido_exer: Optional[float]

    empresa_id: Optional[int] = Field(default=None, foreign_key="empresa.id")
    empresa: Optional[Empresa] = Relationship(back_populates="dados")


# SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

from typing import Optional
from sqlmodel import SQLModel
from datetime import datetime


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


class IDadosdre(SQLModel):
    tri: datetime
    rec_bruta_ope: Optional[float]
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
    desp_operacional: Optional[float]
    desp_admin: Optional[float]
    desp_trib: Optional[float]
    resultado_financeiro: Optional[float]
    receitas_financeiras: Optional[float]
    desp_financeiras: Optional[float]
    res_antes_das_part: Optional[float]
    res_antes_imp_renda: Optional[float]
    contri_social_sobre_lucro: Optional[float]
    imposto_renda: Optional[float]
    result_liquido_exer: Optional[float]

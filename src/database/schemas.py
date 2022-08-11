from pydantic import BaseModel


class IEmpresa(BaseModel):
    id: int
    name: str
    cnpj: str
    ativos: list | None = None

    class Config:
        orm_mode = True

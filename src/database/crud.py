from sqlalchemy import select
from .model import Empresa, Ativo, Session, User


session = Session()


class CRUDUser:
    def __init__(self) -> None:
        self._model = User

    def add(self, username, password):
        user = self._model(username=username, password=password)
        session.add(user)
        session.commit()
        return user

    def get(self, username):
        stmt = select(self._model).where(self._model.username == username)
        user = session.scalars(stmt).first()
        return user


class CRUDEmpresas:
    def __init__(self) -> None:
        self._model = Empresa

    def add(self, name, cnpj):
        emp = self._model(name=name, cnpj=cnpj)
        session.add(emp)
        session.commit()
        return emp

    def get_by_cnpj(self, cnpj):
        stmt = select(self._model).where(self._model.cnpj == cnpj)
        emp = session.scalars(stmt).all()
        return emp


class CRUDAtivos:
    def __init__(self) -> None:
        self._model = Ativo

    def add(self, data, empresa):
        ativo = self._model(data=data, empresa=empresa)
        session.add(ativo)
        session.commit()
        return ativo


# e = CRUDEmpresas()
# emp1 = e.add('Coca-Cola', 234234)
# emp2 = e.add('Pepsi-Cola', 987687)

# a = CRUDAtivos()
# a.add(2342, emp1)

from sqlalchemy import select, or_
from .model import Session, User, Escritorio, Dre, Empresa
# from src.password import get_password_hash
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


class Crud:
    def __init__(self):
        self.session = Session()

    def add_user(self, user_new: str, password: str, escritorios: list | None = None) -> User:
        hash = get_password_hash(password)
        user = User(username=user_new, password=hash)

        if escritorios:
            stmt = select(Escritorio).filter(or_(Escritorio.name == v for v in escritorios))
            escs = self.session.scalars(stmt).all()
            for e in escs:
                user.escritorios.append(e)

        self.session.add(user)
        self.session.commit()
        return user

    def add_escritorio(self, name: str, username: str) -> Escritorio:
        user_model = self.get_user(username)
        e = Escritorio(name=name)
        e.users.append(user_model)
        self.session.add(e)
        self.session.commit()
        return e

    def add_empresa(self, name: str, cnpj: str, escritorio: str) -> Empresa | None:
        stmt = select(Escritorio).where(Escritorio.name == escritorio)
        esc = self.session.scalars(stmt).one_or_none()
        if esc:
            emp = Empresa(name=name, cnpj=cnpj, escritorios=esc)
            self.session.add(emp)
            self.session.commit()
            return e

    def add_dre(self, data: dict, escritorio: str, empresa_name: str, cnpj: str) -> Escritorio | None:
        stmt_esc = select(Escritorio).where(Escritorio.name == escritorio)
        esc = self.session.scalars(stmt_esc).one_or_none()

        stmt_emp = select(Empresa).where(Empresa.name == empresa_name)
        emp = self.session.scalars(stmt_emp).one_or_none()
        if not emp:
            emp = Empresa(name=empresa_name, cnpj=cnpj, escritorio=esc)

        dre = Dre(empresa_rel=emp, **data)
        self.session.add_all([emp, dre])
        self.session.commit()
        return dre

        # stmt = select(Empresa).where(Empresa.name == 'Cola-Cola')
        # emp = self.session.scalars(stmt).one_or_none()
        # if emp:
        #     dre = Dre(empresa_rel=emp, **data)
        #     self.session.add(dre)
        #     self.session.commit()
        #     return dre

    def get_user(self, username: str) -> User:
        stmt = select(User).where(User.username == username)
        user = self.session.scalars(stmt).one_or_none()
        return user

    def get_escritorios(self, username: str) -> list[Escritorio]:
        stmt = select(Escritorio).join(Escritorio.users).where(User.username == username)
        esc = self.session.scalars(stmt).all()
        return esc


# class CRUDEmpresas:
#     def __init__(self) -> None:
#         self._model = Empresa

#     def add(self, name, cnpj):
#         emp = self._model(name=name, cnpj=cnpj)
#         session.add(emp)
#         session.commit()
#         return emp

#     def get_by_cnpj(self, cnpj):
#         stmt = select(self._model).where(self._model.cnpj == cnpj)
#         emp = session.scalars(stmt).all()
#         return emp


# class CRUDAtivos:
#     def __init__(self) -> None:
#         self._model = Ativo

#     def add(self, data, empresa):
#         ativo = self._model(data=data, empresa=empresa)
#         session.add(ativo)
#         session.commit()
#         return ativo


def get_password_hash(texto):
    return pwd_context.hash(texto)


try:
    s = Session()
    c = Crud()
    u = c.add_user('Amim', 'qwer')
    print('ADD USER SUCESSO')
    e = c.add_escritorio('EscritorioA', 'Amim')
    print(f'ADD ESCRITORIO COM SUCESSO: {e}')
    emp = c.add_empresa('Cola-Cola', '09123498257', e.name)
    s.add_all([u, e, emp])
    s.commit()
except Exception as erro:
    print(f'tentou criar user de novo: {erro}')

# e = CRUDEmpresas()
# emp1 = e.add('Coca-Cola', 234234)
# emp2 = e.add('Pepsi-Cola', 987687)

# a = CRUDAtivos()
# a.add(2342, emp1)

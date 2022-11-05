from sqlmodel import Session, select
from .database import engine
from .models import User, Escritorio, Empresa, Dadosdre
from .schemas import IDadosdre
from src.password import get_password_hash
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])


class Crud:
    def get_user(self, username: str):
        stmt = select(User).where(User.username == username)
        with Session(engine) as session:
            user = session.exec(stmt).first()
            return user

    def get_all_users(self):
        stmt = select(User)
        with Session(engine) as session:
            users = session.exec(stmt).all()
            return users

    def get_escritorios_from_user(self, username: str):
        with Session(engine) as session:
            stmt = select(User).where(User.username == username)
            user = session.exec(stmt).one()
            return user.escritorios

    def get_escritorios_and_users_from_user(self, username: str):
        with Session(engine) as session:
            stmt = select(User).where(User.username == username)
            user = session.exec(stmt).one()
            user.escritorios
            return user

    def get_escritorio(self, name: str):
        with Session(engine) as session:
            stmt = select(Escritorio).where(Escritorio.name == name)
            escritorio = session.exec(stmt).one()
            return escritorio

    def get_empresas_from_escritorio(self, name: str):
        with Session(engine) as session:
            stmt = select(Escritorio).where(Escritorio.name == name)
            escritorio = session.exec(stmt).one()
            return escritorio.empresas

    def get_empresa(self, cnpj: str):
        try:
            with Session(engine) as session:
                stmt = select(Empresa).where(Empresa.cnpj == cnpj)
                emp = session.exec(stmt).one()
                return emp
        except Exception:
            return None

    def get_datas_from_empresa(self, cnpj: str):
        try:
            with Session(engine) as session:
                stmt = select(Empresa).where(Empresa.cnpj == cnpj)
                emp = session.exec(stmt).one()
                return emp.dados
        except Exception:
            return []

    def get_datas_from_empresa_name(self, name: str):
        try:
            with Session(engine) as session:
                stmt = select(Empresa).where(Empresa.name == name)
                emp = session.exec(stmt).one()
                return emp.dados
        except Exception:
            return []

    def create_empresa(self, name: str, cnpj: str, escritorio: str):
        emp = Empresa(name=name, cnpj=cnpj)
        with Session(engine) as session:
            stmt = select(Escritorio).where(Escritorio.name == escritorio)
            esc = session.exec(stmt).one()
            emp.escritorio = esc
            session.add(emp)
            session.commit()
            session.refresh(emp)
            return emp

    def create_user(self, name: str, password: str, escritorio: list):
        user = User(username=name, password=get_password_hash("qwer"))
        with Session(engine) as session:
            for x in escritorio:
                stmt = select(Escritorio).where(Escritorio.name == x)
                db_esc = session.exec(stmt).one()
                user.escritorios.append(db_esc)

            session.add(user)
            session.commit()
            session.refresh(user)

    def create_dre(self, dado: IDadosdre, emp: Empresa):
        db_dado = Dadosdre.from_orm(dado)
        db_dado.empresa = emp
        with Session(engine) as session:
            session.add(db_dado)
            session.commit()
            session.refresh(db_dado)
            return db_dado

    def create_escritorio(self, name_escritorio: str, users: list[str]):
        with Session(engine) as session:
            esc = Escritorio(name=name_escritorio)
            for x in users:
                stmt = select(User).where(User.username == x)
                db_user = session.exec(stmt).one()
                esc.users.append(db_user)

            session.add(esc)
            session.commit()
            session.refresh(esc)


try:
    with Session(engine) as session:
        esc = Escritorio(name="Teste")
        password = get_password_hash("admin123")
        user = User(username='admin', password=password)
        user.escritorios.append(esc)
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f'O user criado no inicio: {user}')
except Exception as e:
    print(f'Errro ao criar user inicial: {e}')

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

    def get_escritorios(self, username: str):
        with Session(engine) as session:
            stmt = select(User).where(User.username == username)
            user = session.exec(stmt).one()
            return user.escritorios

    def get_escritorio(self, name: str):
        with Session(engine) as session:
            stmt = select(Escritorio).where(Escritorio.name == name)
            escritorio = session.exec(stmt).one()
            return escritorio

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

    def create_dre(self, dado: IDadosdre, emp: Empresa):
        db_dado = Dadosdre.from_orm(dado)
        db_dado.empresa = emp
        with Session(engine) as session:
            session.add(db_dado)
            session.commit()
            session.refresh(db_dado)
            return db_dado


try:
    with Session(engine) as session:
        esc = Escritorio(name="Jacutinga")
        password = get_password_hash("qwer")
        user = User(username='Amim', password=password)
        user.escritorios.append(esc)
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f'O USER CRIADO NO INICIO: {user}')
except Exception as e:
    print(f'ERRRO AO CRIAR USER INICIAL: {e}')

from sqlmodel import SQLModel, Session
from passlib.context import CryptContext
from src.database.schemas import IDadosdre
from src.password import get_password_hash
from src.data.data_initial import dre, info
from .crud import Crud
from .models import *
from .database import engine

# SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"])

dados1 = IDadosdre(**dre[0])
dados2 = IDadosdre(**dre[1])
dados3 = IDadosdre(**dre[2])
dados4 = IDadosdre(**dre[3])

try:
    crud = Crud()
    with Session(engine) as session:
        esc = Escritorio(name="XFictícia")
        password = get_password_hash("qwER12#$")
        user = User(username="admin", password=password, is_admin=True)
        user.escritorios.append(esc)
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"O user criado no inicio: {user}")
        emp = crud.create_empresa(info["name"], info["cnpj"], info["escritorio"])
        print(f"A EMP FOI CRIADA: {emp}")
        crud.create_dre(dados1, emp)
        crud.create_dre(dados2, emp)
        crud.create_dre(dados3, emp)
        crud.create_dre(dados4, emp)
except Exception as e:
    print(f"Errro ao criar user inicial: {e}")

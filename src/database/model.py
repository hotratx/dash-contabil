from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
# from src.password import get_password_hash


engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False}, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(String(150))
    escritorios = relationship('Escritorio', secondary='escritorio_users', back_populates='users')

    def __repr__(self):
        return f"username={self.username}"


class Escritorio(Base):
    __tablename__ = "escritorios"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    users = relationship('User', secondary='escritorio_users', back_populates='escritorios')
    empresas = relationship("Empresa", back_populates="escritorio")


class EscritorioUser(Base):
    __tablename__ = "escritorio_users"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    escritorio_id = Column(Integer, ForeignKey('escritorios.id'))


class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    cnpj = Column(String(30))
    escritorio_id = Column(Integer, ForeignKey("escritorios.id"))
    escritorio = relationship("Escritorio", back_populates="empresas")
    dres = relationship("Dre", back_populates="empresa")

    def __repr__(self):
        return f"cnpj: cnpj={self.cnpj}, rbo={self.rbo}"


class Dre(Base):
    __tablename__ = "dre"
    id = Column(Integer, primary_key=True)
    rbo = Column(Float, nullable=True)
    fpms = Column(Float, nullable=True)
    vm = Column(Float, nullable=True)
    dr = Column(Float, nullable=True)
    ifs = Column(Float, nullable=True)
    icms = Column(Float, nullable=True)
    cofins = Column(Float, nullable=True)
    pis = Column(Float, nullable=True)
    od = Column(Float, nullable=True)
    vcddi = Column(Float, nullable=True)
    rl = Column(Float, nullable=True)
    cmspv = Column(Float, nullable=True)
    cmr = Column(Float, nullable=True)
    lb = Column(Float, nullable=True)
    do = Column(Float, nullable=True)
    da = Column(Float, nullable=True)
    dt = Column(Float, nullable=True)
    rfo = Column(Float, nullable=True)
    rfs = Column(Float, nullable=True)
    df = Column(Float, nullable=True)
    rapc = Column(Float, nullable=True)
    raircs = Column(Float, nullable=True)
    cssl = Column(Float, nullable=True)
    ir = Column(Float, nullable=True)
    rle = Column(Float, nullable=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    empresa = relationship("Empresa", back_populates="dres")

    def __repr__(self):
        return f"Dre(id={self.empresa_id}, data={self.rbo})"


Base.metadata.create_all(engine)

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from src.password import get_password_hash


engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False}, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    password = Column(String(150))

    def __repr__(self):
        return f"username={self.username}"


class Empresa(Base):
    __tablename__ = "empresa"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    cnpj = Column(String(30))
    dres = relationship("Dre", back_populates="empresa")

    def __repr__(self):
        return f"cnpj: cnpj={self.cnpj}, rbo={self.rbo}"


class Dre(Base):
    __tablename__ = "dre"
    id = Column(Integer, primary_key=True)
    rbo = Column(Float, nullable=True)
    fpms = Column(Float, nullable=True)
    # vm = Column(Float, precision=2, nullable=True)
    # dr = Column(Float, precision=2, nullable=True)
    # ifs = Column(Float, precision=2, nullable=True)
    # icms = Column(Float, precision=2, nullable=True)
    # cofins = Column(Float, precision=2, nullable=True)
    # pis = Column(Float, precision=2, nullable=True)
    # od = Column(Float, precision=2, nullable=True)
    # vcddi = Column(Float, precision=2, nullable=True)
    # rl = Column(Float, precision=2, nullable=True)
    # cmspv = Column(Float, precision=2, nullable=True)
    # cmr = Column(Float, precision=2, nullable=True)
    # lb = Column(Float, precision=2, nullable=True)
    # do = Column(Float, precision=2, nullable=True)
    # da = Column(Float, precision=2, nullable=True)
    # dt = Column(Float, precision=2, nullable=True)
    # rfo = Column(Float, precision=2, nullable=True)
    # rfs = Column(Float, precision=2, nullable=True)
    # df = Column(Float, precision=2, nullable=True)
    # rapc = Column(Float, precision=2, nullable=True)
    # raircs = Column(Float, precision=2, nullable=True)
    # cssl = Column(Float, precision=2, nullable=True)
    # ir = Column(Float, precision=2, nullable=True)
    # rle = Column(Float, precision=2, nullable=True)
    empresa_id = Column(Integer, ForeignKey("empresa.id"))
    empresa = relationship("Empresa", back_populates="dres")

    def __repr__(self):
        return f"Dre(id={self.empresa_id}, data={self.rbo})"


Base.metadata.create_all(engine)

password = get_password_hash("qwer")
user = User(username="Matheus", password=password)

# emp1 = Empresa(name='Coca-Cola', cnpj=212345)
# emp2 = Empresa(name='Pesi-Cola', cnpj=763874)

# ativo1 = Ativo(data=1234, empresa=emp1)

with Session() as session:
    # session.add_all([emp1, emp2, ativo1])
    session.add(user)
    session.commit()

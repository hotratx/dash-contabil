from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine("sqlite:///test.db", echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


s = Session()

class Ativo(Base):
    __tablename__ = "ativos"
    id = Column(Integer, primary_key=True)
    data = Column(Integer)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    empresa = relationship('Empresa')

    def __repr__(self):
        return f"Ativo(empresa={self.empresa}, data={self.data})"


class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    cnpj = Column(String(30))
    ativos = relationship(Ativo, backref="empresas")

    def __repr__(self):
        return f"cnpj: cnpj={self.cnpj}, ativos={self.ativos}"



Base.metadata.create_all(engine)


# emp1 = Empresa(name='Coca-Cola', cnpj=212345)
# emp2 = Empresa(name='Pesi-Cola', cnpj=763874)

# ativo1 = Ativo(data=1234, empresa=emp1)

# with Session() as session:
#     session.add_all([emp1, emp2, ativo1])
#     session.commit()

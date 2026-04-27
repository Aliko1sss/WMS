from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase


# ✅ Создаём Base как подкласс DeclarativeBase
class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Float, default=0.0)


class Operation(Base):
    __tablename__ = "operations"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    op_type = Column(String, nullable=False)  # IN или OUT
    amount = Column(Float, nullable=False)

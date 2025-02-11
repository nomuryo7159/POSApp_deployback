from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass

from typing_extensions import Annotated
from sqlalchemy.sql import text

timestamp = Annotated[
    datetime,
    mapped_column(DateTime(timezone=True), server_default=text("NOW()")),
]

class Master(Base):
    __tablename__ = 'master_nomurin'
    prd_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(10))
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)


class Purchases(Base):
    __tablename__ = 'purchases_nomurin'
    trd_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    datetime: Mapped[timestamp] = mapped_column(DateTime(timezone=True), nullable=False)
    emp_cd: Mapped[str] = mapped_column(String(10))
    store_cd: Mapped[str] = mapped_column(String(10))
    pos_no: Mapped[str] = mapped_column(String(10))
    total_amt: Mapped[int] = mapped_column(Integer)


class PurchaseDetails(Base):
    __tablename__ = 'purchase_details_nomurin'
    trd_id: Mapped[int] = mapped_column(Integer, ForeignKey('purchases_nomurin.trd_id'))
    dtl_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    prd_id: Mapped[int] = mapped_column(Integer, ForeignKey('master_nomurin.prd_id'))
    prd_code: Mapped[str] = mapped_column(String(10))
    prd_name: Mapped[str] = mapped_column(String(100))
    prd_price: Mapped[int] = mapped_column(Integer)

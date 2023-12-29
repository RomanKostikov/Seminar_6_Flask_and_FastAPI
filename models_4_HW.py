from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Numeric,
    ForeignKey,
    Date,
)


# Pydantic models
class UserIn(BaseModel):
    name: str
    last_name: str
    email: str
    password: str


class UserOut(UserIn):
    id: int


class ItemIn(BaseModel):
    title: str
    description: str
    price: Decimal


class ItemOut(ItemIn):
    id: int


class OrderIn(BaseModel):
    user_id: int
    item_id: int
    order_date: date
    delivered: bool = False


class OrderOut(OrderIn):
    id: int


# SQLalchemy models

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    orders = relationship('Order', backref='user')


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(scale=2), nullable=False)
    orders = relationship('Order', backref='item')


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    item_id = Column(Integer, ForeignKey('item.id'))
    order_date = Column(Date, nullable=False)
    delivered = Column(Boolean, nullable=False, default=False)
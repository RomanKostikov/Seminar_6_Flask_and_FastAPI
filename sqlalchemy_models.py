from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, Date

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)


class User2(Base):
    __tablename__ = 'users_2'

    id = Column(Integer, primary_key=True)
    name = Column(String(3))
    last_name = Column(String(3))
    email = Column(String)
    birthdate = Column(Date)
    address = Column(String(5))

from pydantic import BaseModel, Field
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean


class TaskIn(BaseModel):
    title: str = Field()
    description: str | None = Field(default=None)
    done: bool = Field(default=False)


class TaskOut(TaskIn):
    id: int


# sqlalchemy models
Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    done = Column(Boolean, default=False)

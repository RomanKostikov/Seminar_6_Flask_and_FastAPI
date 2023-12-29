# Задание №2
# Создать веб-приложение на FastAPI, которое будет предоставлять API для
# работы с базой данных пользователей. Пользователь должен иметь
# следующие поля:
# ○ ID (автоматически генерируется при создании пользователя)
# ○ Имя (строка, не менее 2 символов)
# ○ Фамилия (строка, не менее 2 символов)
# ○ Дата рождения (строка в формате "YYYY-MM-DD")
# ○ Email (строка, валидный email)
# ○ Адрес (строка, не менее 5 символов)
# API должен поддерживать следующие операции:
# ○ Добавление пользователя в базу данных
# ○ Получение списка всех пользователей в базе данных
# ○ Получение пользователя по ID
# ○ Обновление пользователя по ID
# ○ Удаление пользователя по ID
# Приложение должно использовать базу данных SQLite3 для хранения
# пользователей.
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import create_engine, select, insert, update, delete
import databases

from pydantic_models import UserIn, UserOut
from sqlalchemy_models import Base, User2

DATABASE_URL = 'sqlite:///task_1.sqlite'

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()

    yield

    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get('/', response_model=list[UserOut])
async def index():
    users = select(User2)

    return await database.fetch_all(users)


@app.post('/users/')
async def create_user(user: UserIn):
    new_user = insert(User2).values(
        name=user.name,
        last_name=user.last_name,
        email=user.email,
        birthdate=user.birthdate,
        address=user.address,
    )
    await database.execute(new_user)

    return {**user.model_dump()}
    # return {'result': 'ok'}


@app.get('/users/{user_id}', response_model=UserOut)
async def get_user(user_id: int):
    user = await database.fetch_one(select(User2).where(User2.id == user_id))

    return user


@app.put('/users/{user_id}', response_model=UserOut)
async def update_user(user_id: int, new_user: UserIn):
    user_update = (
        update(User2)
        .where(User2.id == user_id)
        .values(**new_user.model_dump())
    )
    await database.execute(user_update)

    return await database.fetch_one(select(User2).where(User2.id == user_id))


@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    delete_user = delete(User2).where(User2.id == user_id)

    await database.execute(delete_user)

    return {'result': 'success', 'deleted_user_id': user_id}

# Задание №1
# Разработать API для управления списком пользователей с
# использованием базы данных SQLite. Для этого создайте
# модель User со следующими полями:
# ○ id: int (идентификатор пользователя, генерируется
# автоматически)
# ○ username: str (имя пользователя)
# ○ email: str (электронная почта пользователя)
# ○ password: str (пароль пользователя)
# API должно поддерживать следующие операции:
# ○ Получение списка всех пользователей: GET /users/
# ○ Получение информации о конкретном пользователе: GET /users/{user_id}/
# ○ Создание нового пользователя: POST /users/
# ○ Обновление информации о пользователе: PUT /users/{user_id}/
# ○ Удаление пользователя: DELETE /users/{user_id}/
# Для валидации данных используйте параметры Field модели User.
# Для работы с базой данных используйте SQLAlchemy и модуль databases.

from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import create_engine, select, insert, update, delete
import databases

from pydantic_models import UserOnRegister, User
from sqlalchemy_models import Base, User as SUser

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


@app.get('/', response_model=list[User])
async def index():
    users = select(SUser)

    return await database.fetch_all(users)


@app.post('/users/', response_model=UserOnRegister)
async def create_user(user: UserOnRegister):
    new_user = insert(SUser).values(**user.model_dump())
    await database.execute(new_user)

    return new_user


@app.get('/users/{user_id}', response_model=User)
async def get_user(user_id: int):
    user = await database.fetch_one(select(SUser))

    return user


@app.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, new_user: UserOnRegister):
    user_update = (
        update(SUser)
        .where(SUser.id == user_id)
        .values(**new_user.model_dump())
    )
    await database.execute(user_update)

    return await database.fetch_one(select(SUser).where(SUser.id == user_id))


@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    delete_user = delete(SUser).where(SUser.id == user_id)

    await database.execute(delete_user)

    return {'result': 'success', 'deleted_user_id': user_id}

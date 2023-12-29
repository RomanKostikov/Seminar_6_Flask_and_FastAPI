# Задание №6
# Необходимо создать базу данных для интернет-магазина. База данных должна
# состоять из трех таблиц: товары, заказы и пользователи. Таблица товары должна
# содержать информацию о доступных товарах, их описаниях и ценах. Таблица
# пользователи должна содержать информацию о зарегистрированных
# пользователях магазина. Таблица заказы должна содержать информацию о
# заказах, сделанных пользователями.
# ○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
# имя, фамилия, адрес электронной почты и пароль.
# ○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
# название, описание и цена.
# ○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
# пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
# заказа.
# Создайте модели pydantic для получения новых данных и
# возврата существующих в БД для каждой из трёх таблиц
# (итого шесть моделей).
# Реализуйте CRUD операции для каждой из таблиц через
# создание маршрутов, REST API (итого 15 маршрутов).
# ○ Чтение всех
# ○ Чтение одного
# ○ Запись
# ○ Изменение
# ○ Удаление
from contextlib import asynccontextmanager
import databases
from fastapi import FastAPI
from sqlalchemy import create_engine, select, insert, update, delete

from models_4_HW import (
    Base,
    UserIn,
    UserOut,
    ItemIn,
    ItemOut,
    OrderIn,
    OrderOut,
    User,
    Item,
    Order,
)

DATABASE_URL = 'sqlite:///task_4_HW.sqlite'

db = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()

    yield

    await db.disconnect()


app = FastAPI(lifespan=lifespan, title='Задание 6', version='1.0')


# Get all the records from the database
@app.get('/')
async def index():
    users = await db.fetch_all(select(User))
    users = [UserOut.model_validate({
        'id': user.id,
        'name': user.name,
        'last_name': user.last_name,
        'email': user.email,
        'password': user.password
    }) for user in users]

    items = await db.fetch_all(select(Item))
    items = [ItemOut.model_validate({
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'price': item.price
    }) for item in items]

    orders = await db.fetch_all(select(Order))
    orders = [OrderOut.model_validate({
        'id': order.id,
        'user_id': order.user_id,
        'item_id': order.item_id,
        'order_date': order.order_date,
        'delivered': order.delivered
    }) for order in orders]

    return {'users': users, 'items': items, 'orders': orders}


# Users CRUD operations
@app.get('/users/', response_model=list[UserOut])
async def get_users():
    return await db.fetch_all(select(User))


@app.post('/users/', response_model=UserIn)
async def create_user(user: UserIn):
    new_user = insert(User).values(**user.model_dump())

    await db.execute(new_user)

    return user


@app.get('/users/{user_id}/', response_model=UserOut)
async def get_user(user_id: int):
    return await db.fetch_one(select(User).where(User.id == user_id))


@app.put('/users/{user_id}/', response_model=UserOut)
async def edit_user(user_id: int, new_user: UserIn):
    user_update = (
        update(User)
        .where(User.id == user_id)
        .values(**new_user.model_dump())
    )
    await db.execute(user_update)

    return await db.fetch_one(select(User).where(User.id == user_id))


@app.delete('/users/{user_id}/')
async def delete_user(user_id: int):
    delete_user = delete(User).where(User.id == user_id)

    await db.execute(delete_user)

    return {'deleted': True, 'deleted_user_id': user_id}


# Items CRUD operations
@app.get('/items/', response_model=list[ItemOut])
async def get_items():
    return await db.fetch_all(select(Item))


@app.post('/items/', response_model=ItemIn)
async def create_item(item: ItemIn):
    new_item = insert(Item).values(**item.model_dump())

    await db.execute(new_item)

    return item


@app.get('/items/{item_id}/', response_model=ItemOut)
async def get_item(item_id: int):
    return await db.fetch_one(select(Item).where(Item.id == item_id))


@app.put('/items/{item_id}/', response_model=ItemOut)
async def edit_item(item_id: int, new_item: ItemIn):
    item_update = (
        update(Item)
        .where(Item.id == item_id)
        .values(**new_item.model_dump())
    )

    await db.execute(item_update)

    return await db.fetch_one(select(Item).where(Item.id == item_id))


@app.delete('/items/{item_id}/', response_model=ItemOut)
async def delete_item(item_id: int):
    delete_item = delete(Item).where(Item.id == item_id)

    await db.execute(delete_item)

    return {'deleted': True, 'deleted_item_id': item_id}


# Orders CRUD operations
@app.get('/orders/', response_model=list[OrderOut])
async def get_orders():
    return await db.fetch_all(select(Order))


@app.post('/orders/', response_model=OrderIn)
async def create_order(order: OrderIn):
    new_order = insert(Order).values(**order.model_dump())

    await db.execute(new_order)

    return order


@app.get('/orders/{order_id}/', response_model=OrderOut)
async def get_order(order_id: int):
    return await db.fetch_one(select(Order).where(Order.id == order_id))


@app.put('/orders/{order_id}/', response_model=OrderOut)
async def edit_order(order_id: int, new_order: OrderIn):
    order_update = (
        update(Order)
        .where(Order.id == order_id)
        .values(**new_order.model_dump())
    )

    await db.execute(order_update)

    return await db.fetch_one(select(Order).where(Order.id == order_id))


@app.delete('/orders/{order_id}/', response_model=OrderOut)
async def delete_order(order_id: int):
    delete_order = delete(Order).where(Order.id == order_id)

    await db.execute(delete_order)

    return {'deleted': True, 'deleted_order_id': order_id}

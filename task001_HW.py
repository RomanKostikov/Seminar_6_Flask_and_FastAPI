# Задание №3
# Создать API для управления списком задач.
# Каждая задача должна содержать поля "название",
# "описание" и "статус" (выполнена/не выполнена).
# API должен позволять выполнять CRUD операции с
# задачами.
from contextlib import asynccontextmanager
import databases
from fastapi import FastAPI
from sqlalchemy import create_engine, select, insert, update, delete

from models_1_HW import TaskIn, TaskOut, Base, Task

DATABASE_URL = 'sqlite:///task_1_HW.sqlite'

db = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()

    yield

    await db.disconnect()


app = FastAPI(lifespan=lifespan)


# Functions that returns a list of tasks
@app.get('/', response_model=list[TaskOut])
async def index():
    tasks = select(Task)

    return await db.fetch_all(tasks)


@app.get('/completed/', response_model=list[TaskOut])
async def get_completed():
    tasks = select(Task).where(Task.status == True)

    return await db.fetch_all(tasks)


@app.get('/uncompleted/', response_model=list[TaskOut])
async def get_uncompleted():
    tasks = select(Task).where(Task.status == False)

    return await db.fetch_all(tasks)


# Functions for edit the whole task information
@app.post('/tasks/', response_model=TaskIn)
async def create_task(task: TaskIn):
    new_task = insert(Task).values(**task.model_dump())
    await db.execute(new_task)

    return task


@app.get('/tasks/{task_id}/', response_model=TaskOut)
async def get_task(task_id: int):
    task = await db.fetch_one(select(Task).where(Task.id == task_id))

    return task


@app.put('/tasks/{task_id}/', response_model=TaskOut)
async def update_task(task_id: int, task: TaskIn):
    task_update = (
        update(Task).where(Task.id == task_id).values(**task.model_dump())
    )
    await db.execute(task_update)

    return await db.fetch_one(select(Task).where(Task.id == task_id))


@app.delete('/tasks/{task_id}/')
async def delete_task(task_id: int):
    sql_task = await db.fetch_one(select(Task).where(Task.id == task_id))
    task = TaskOut.model_validate(
        {
            'id': sql_task.id,
            'title': sql_task.title,
            'description': sql_task.description,
            'done': sql_task.done
        }
    )

    task_delete = delete(Task).where(Task.id == task_id)
    await db.execute(task_delete)

    return {'deleted': True, 'task': task.model_dump()}


# Function for marking a task as completed
@app.post('/tasks/{task_id}/complete/', response_model=TaskOut)
async def complete_task(task_id: int):
    task_complete = (
        update(Task).where(Task.id == task_id).values(status=True)
    )
    await db.execute(task_complete)

    return await db.fetch_one(select(Task).where(Task.id == task_id))
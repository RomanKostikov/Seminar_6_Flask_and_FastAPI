from datetime import date
from pydantic import BaseModel, Field


# модель User со следующими полями:
# id: int (идентификатор пользователя, генерируется автоматически)
# username: str (имя пользователя)
# email: str (электронная почта пользователя)
# password: str (пароль пользователя)
class UserOnRegister(BaseModel):
    username: str
    email: str
    password: str


class User(UserOnRegister):
    id: int


# ID (автоматически генерируется при создании пользователя)
# Имя (строка, не менее 2 символов)
# Фамилия (строка, не менее 2 символов)
# Дата рождения (строка в формате "YYYY-MM-DD")
# Email (строка, валидный email)
# Адрес (строка, не менее 5 символов)
class UserIn(BaseModel):
    name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    email: str
    birthdate: date = Field(None)
    address: str = Field(min_length=5)


class UserOut(UserIn):
    id: int
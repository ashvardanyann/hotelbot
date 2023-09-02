from peewee import *

# Подключаемся либо создаем базу данных SQLite
db = SqliteDatabase('bot_db.db')


class BaseModel(Model):
    """Создаем базовый модель таблицы со столбцом id"""
    id = AutoField(primary_key=True)

    class Meta:
        database = db


class User(BaseModel):
    """Создаем модель таблицы User со столбцами id, tg_user_id, start_datetime"""
    tg_user_id = IntegerField()
    user_name = CharField()
    start_datetime = DateTimeField()

    class Meta:
        table_name = 'users'  # название таблицы


class History(BaseModel):
    """Создаем модель таблицы History со столбцами id, user_id, request_datetime..."""
    user_id = ForeignKeyField(User)
    request_datetime = DateTimeField()
    command_type = CharField()
    region = CharField()
    results_size = IntegerField()
    check_in_date = CharField()
    check_out_date = CharField()
    adults = IntegerField()
    children = CharField()
    price = CharField()

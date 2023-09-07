import peewee as pw

# Подключаемся либо создаем базу данных SQLite
db = pw.SqliteDatabase('bot_db.db')


class BaseModel(pw.Model):
    """Создаем базовый модель таблицы со столбцом id"""
    id = pw.AutoField(primary_key=True)

    class Meta:
        database = db


class User(BaseModel):
    """Создаем модель таблицы User со столбцами id, tg_user_id, start_datetime"""
    tg_user_id = pw.IntegerField()
    user_name = pw.CharField()
    start_datetime = pw.DateTimeField()

    class Meta:
        table_name = 'users'  # название таблицы


class History(BaseModel):
    """Создаем модель таблицы History со столбцами id, user_id, request_datetime..."""
    user_id = pw.ForeignKeyField(User)
    request_datetime = pw.DateTimeField()
    command_type = pw.CharField()
    region = pw.CharField()
    results_size = pw.IntegerField()
    check_in_date = pw.CharField()
    check_out_date = pw.CharField()
    adults = pw.IntegerField()
    children = pw.CharField()
    price = pw.CharField()

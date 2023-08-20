from peewee import *


db = SqliteDatabase('bot_db.db')


class BaseModel(Model):
    id = AutoField(primary_key=True)

    class Meta:
        database = db


class User(BaseModel):
    tg_user_id = IntegerField()
    user_name = CharField()
    start_datetime = DateTimeField()

    class Meta:
        table_name = 'users'


class History(BaseModel):
    user_id = ForeignKeyField(User)
    request_datetime = DateTimeField()
    command_tipe = CharField()
    region = CharField()
    results_size = IntegerField()
    check_in_date = DateField()
    check_out_date = DateField()
    adults = IntegerField()
    children = CharField()
    price = IntegerField()

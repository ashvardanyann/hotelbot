from peewee import *
import datetime

db = SqliteDatabase('bot_db.db')


class BaseModel(Model):
    id = AutoField(primary_key=True)

    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField()
    user_name = CharField()
    start_date = DateTimeField()

    class Meta:
        table_name = 'Users'


with db:
    db.create_tables([User])
    User(user_id=123123113, user_name = "asdasd", start_date=datetime.datetime.now()).save()

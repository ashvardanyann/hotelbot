from .models import *
import datetime


class DataBase:
    @staticmethod
    def create_db():
        db.create_tables([User, History])

    @staticmethod
    def _user_exists(tg_user_id):
        with db:
            return bool(User.select().where(User.tg_user_id == tg_user_id))

    def add_user(self, tg_user_id, user_name):
        # print(self._user_exists(tg_user_id))
        if not self._user_exists(tg_user_id):
            with db:
                User(tg_user_id=tg_user_id,
                     user_name=user_name,
                     start_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).save()
        # with db:
        #     row = User.get(User.tg_user_id == tg_user_id)
        #     print(type(row.start_datetime))

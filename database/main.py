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
        with db:
            row = User.get(User.tg_user_id == tg_user_id)
            print(row.id)

    @staticmethod
    def save_action(tg_user_id, request_info, price="0"):
        with db:
            user_start_info = User.get(User.tg_user_id == tg_user_id)
            # print(user_start_info.id)
            History(user_id=user_start_info,
                    request_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    command_type=request_info['price_type'],
                    region=request_info['region'],
                    results_size=request_info['results_size'],
                    check_in_date=request_info['check_in_data'],
                    check_out_date=request_info['check_out_data'],
                    adults=request_info['adults'],
                    children=request_info['children'],
                    price=price).save()

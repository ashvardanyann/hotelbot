from .models import db, User, History
import datetime


class DataBase:
    """Класс для работы с базой данных"""
    @staticmethod
    def create_db():
        """На основе моделей таблиц создаем таблицы users и history"""
        db.create_tables([User, History])

    @staticmethod
    def _user_exists(tg_user_id):
        """Проверяем есть ли пользователь с tg_user_id в базе данных если есть то возвращаем True в противном случае
        False"""
        with db:
            return bool(User.select().where(User.tg_user_id == tg_user_id))

    def add_user(self, tg_user_id, user_name):
        """Добавляем пользователя с tg_user_id в бау данных"""
        if not self._user_exists(tg_user_id):  # проверяем есть ли пользователь с tg_user_id в БД если нет то добавляем
            with db:
                User(tg_user_id=tg_user_id,
                     user_name=user_name,
                     start_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).save()

    @staticmethod
    def save_action(tg_user_id, request_info, price="0"):
        """Сохраняем всю информацию запроса в базе данных"""
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

    @staticmethod
    def get_history(tg_user_id):
        """Возвращаем историю последних 10 запросов пользователя"""
        with db:
            user_id = User.get(User.tg_user_id == tg_user_id).id
            user_requests = History.select().where(History.user_id == user_id).order_by(History.id.desc()).limit(10)
            text = ""
            num = 1
            for data in reversed(user_requests):
                text += (f"{abs(num)} <b>{data.region}</b> | кол.отелей: <b>{data.results_size}</b>\n | заезд: <b>{data.check_in_date}</b>\n | "
                         f"выезд: <b>{data.check_out_date}</b>\n | взрослые: <b>{data.adults}</b>\n | возрасты детей: <b>{data.children}</b>\n")
                if data.command_type == "low":
                    text += f" | цены: <b>дешевые</b>\n\n"
                elif data.command_type == "high":
                    text += f" | цены: <b>дорогие</b>\n\n"
                elif data.command_type == "custom":
                    text += f" | цены: <b>{data.price}</b>$\n\n"
                num += 1

            return text

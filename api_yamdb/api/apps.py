from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'
    verbose_name = 'Функции апи'

class TitlesConfig(AppConfig):
    name = 'titles'
    verbose_name = 'Произведения'

class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Пользователи'

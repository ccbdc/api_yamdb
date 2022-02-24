ОПИСАНИЕ:
Проект собирает отзывы пользователей о различных произведениях.

КАК ЗАПУСТИТЬ:

Клонировать реп командами
git clone git@github.com...
cd api_yamdb

Создать виртуальное окружение и активировать его командами
python3 -m venv venv
source venv/bin/activate

Установить зависимости командами
python3 -m pip install --upgrade pip
pip install -r requirements.txt

Выполнить миграции командами
python3 manage.py migrate

Запустить проект командами
python3 manage.py runserver
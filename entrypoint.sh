#!/bin/sh
python shorturl/manage.py makemigrations app
# Ожидание доступности базы данных
sleep 15
# Применение миграций
python shorturl/manage.py migrate

# Добавление первого кода в CodeState после миграции
python shorturl/manage.py shell -c "from shortener.models import CodeState; CodeState.objects.create(last_code='aaaaaaaa')"

# Запуск Django приложения
python shorturl/manage.py runserver 0.0.0.0:8000
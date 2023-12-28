# Первоначальные настройки
Создать .env файл в корневой директории проекта с содержимым
```
POSTGRES_DB = example_db
POSTGRES_USER = example_user
POSTGRES_PASSWORD = example_password
```
Данные из примера нужно заменить на свои
В shorturl/shorturl/settings.py при необходимости указать доменный адрес(по умолчанию локальный адрес)
# Запуск приложения
С помощью консоли перейти в корневую директорию и выполнить
```
docker-compose up
```
# Работа с приложением
Администратор может удалять ссылки, которые не использовались какое-то количество дней с помощью команды
```
python manage.py cleanup_links 30 
```
Вместо 30 можно указать любое неотрицательное число дней

По умолчанию документация находится по адресу
```
http://127.0.0.1:8000/api/schema/swagger-ui/
```
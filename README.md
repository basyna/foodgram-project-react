![example workflow](https://github.com/basyna/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Цель работы

Проект Foodgram-продуктовый помощник, позволяет публиковать и обмениваться рецептами пользователям, коллекционировать любимые рецепты, подписываться на авторов рецептов, формировать список покупок по выбранным рецептам.

### Задача: реализовать backend проекта 

---------------------------------------------------------------

## Технологии, использованные при выполнении работы:

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green"/>
<img src="https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white"/>

<img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white"/>
<img src="https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white"/>

------------------------------------------------------------------

## Развётывание

Что бы развернуть приложение проделайте следующие шаги:

Склонируйте репозиторий.
```
git clone https://github.com/basyna/foodgram-project-react
```

Перейдити в папку infra и создайте _.env_ файл:
```
cd foodgram-project-react/infra
nano .env
```


Для корректной работы сервиса файл _.env_ в папке infra, должен быть наполнен секретными данными по шаблону:

```
DJANGO_KEY=default-key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=login
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
```
_DJANGO_KEY_ должен представлять собой строку из 50 случайных символов для обеспечения безопасности.

Сформировать его можно в консоли интерактивного режима Django
```
$ python manage.py shell

>>> from django.core.management.utils import get_random_secret_key
>>> get_random_secret_key()
```

Запустите сборку контейнеров (при установленном и запущенном Docker):
```
docker-compose up -d --build
```
В контейнере web выполните миграции:
```
docker-compose exec web python manage.py migrate 
```
Создатйте суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
Или для GIT BASH в Windows:
```
winpty docker-compose exec web python manage.py createsuperuser
```

Соберите статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
Проект запущен и доступен по адресу: [localhost](#http://localhost/admin/)

## Загрузка тестовых значений в БД

Загрузить тестовые данные из файла JSON в БД:

```
docker-compose exec web python manage.py loaddata fixtures.json
```

--------------------------------------------------------------------

## Об авторе

Автор работы: - [Борис Сенкевич](https://github.com/basyna), студент 38 когорты курса Python разработчик

Этот проект был создан в качестве задания на платформе [Яндекс Практикум](https://practicum.yandex.ru/)

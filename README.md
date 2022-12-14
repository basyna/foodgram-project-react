![example workflow](https://github.com/basyna/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Дипломный проект Docker
## Проект доступен по адресу [51.250.108.25](http://51.250.108.25/redoc/)

## Цель работы

Проект Foodgram собирает отзывы (Review) пользователей на произведения (Title). Произведения делятся на категории (Genre). Список категорий может быть расширен администратором.

Задача: развернуть этот сервис в Docker

---------------------------------------------------------------

## Технологии, использованные при выполнении работы:

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green"/>
<img src="https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white"/>
<img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white"/>
<img src="https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white"/>

------------------------------------------------------------------


## Алгоритм регистрации пользователей
  1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
  2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес  `email`.
  3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
  4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

### Пользовательские роли
  - **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
  - **Аутентифицированный пользователь** (`user`) — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять **свои** отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
  - **Модератор** (`moderator`) — те же права, что и у **Аутентифицированного пользователя** плюс право удалять **любые** отзывы и комментарии.
  - **Администратор** (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям. 
  - **Суперюзер Django** — обладет правами администратора (`admin`)
--------------------------------------------------------------------

## Развётывание

Что бы развернуть приложение проделайте следующие шаги:

Склонируйте репозиторий.
```
git clone https://github.com/basyna/yamdb_final
```

Перейдити в папку infra и создайте _.env_ файл:
```
cd yamdb_final/infra
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
docker-compose up -d
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

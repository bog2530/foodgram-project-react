# Foodgram, «Продуктовый помощник».
[![Django-app workflow](https://github.com/bog2530/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/bog2530/foodgram-project-react/actions/workflows/main.yml)
### Технологии
- Python == 3.9
- Django == 2.2
- DRF == 3.12
- PEP8
- PostgreSQL
- Docker
- Docker-compose
- Gunicorn
- Nginx
- React
- Яндекс.Облако


## Описание
«Продуктовый помощник».: сайт, на котором пользователи будут публиковать рецепты,
добавлять чужие рецепты в избранное и подписываться на публикации других авторов.
Сервис «Список покупок» позволит пользователям создавать список продуктов,
которые нужно купить для приготовления выбранных блюд.

## Как работает проект
- Проект работает с СУБД PostgreSQL.
- Проект запущен на сервере в Яндекс. 
Облаке в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn. 
Заготовленный контейнер с фронтендом используется для сборки файлов.
- Контейнер с проектом обновляется на Docker Hub.
- В nginx настроена раздача статики, запросы с фронтенда переадресуются в контейнер с Gunicorn. 
Джанго-админка работает напрямую через Gunicorn.

## Как запустить
### Запуск через docker-compose:  
```
docker-compose up -d --build
```
##### Выполнить миграции:
```  
docker-compose exec web python manage.py migrate  
```  
##### Cоздать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
##### Собрать статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```

## Примеры запросов:
 - [GET] http://localhost/api/recipes/
- 200
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```
 - [GET] http://localhost/api/tags/
 - 200
```
[
    {
    "id": 0,
    "name": "Завтрак",
    "color": "#E26C2D",
    "slug": "breakfast"
    }
]
```
 - [POST] http://localhost/api/recipes/{id}/favorite/
 - 201
 ```
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
```

## Документация:
  [Документация](http://localhost/api/docs/) доступна при запуске через docker-compose


## Автор
[Шумский Богдан](https://github.com/bog2530)
Telegram: [@bog2530](https://t.me/bog2530)
Email: bog2530@gmail.com
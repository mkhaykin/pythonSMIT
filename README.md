# python SMIT

## Тестовое задание.
Требуется реализовать REST API сервис по расчёту стоимости страхования в зависимости от типа груза и объявленной
стоимости (ОС). [Полное описание](docs/Python_SMIT.pdf).

Стек: FastApi, SqlAlchemy, Postgresql, Docker, Docker-compose.

## Ограничения.
База postgres создается прямо в контейнере (полагаю для тестового проекта это допустимо).  

Загрузка данных производится с полной очисткой таблицы от старых данных.

Формат загрузки взят из ТЗ:
```json
{
    "2020-06-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.04"
        },
        {
            "cargo_type": "Other",
            "rate": "0.01"
        }
    ],
    "2020-07-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.035"
        },
        {
            "cargo_type": "Other",
            "rate": "0.015"
        }
    ]
}
```
В процессе сохранения и поиска тип груза приводится к нижнему регистру.

В ТЗ не было указаний нужно ли при поиске типа груза использовать "Other" как 
дефолтное значение для ненайденных грузов, поэтому в решении ищется по полному 
совпадению. При отсутствии тарифа возвращается ошибка 404.

## Тестирование решения.
АPI разворачивается на 8000 порту (локальный доступ http://0.0.0.0:8000 )  
Postgres в отдельном контейнере, порт задается в переменных среды.

### Переменные среды:
Для запуска и тестирования проекта, требуется создать файл `.env` с переменными окружения.\
Пример файла: `.env.example`

### Параметры postgres:
- `POSTGRES_HOST` - имя хоста
- `POSTGRES_PORT` - порт
- `POSTGRES_DB` - имя базы данных
- `POSTGRES_USER` - пользователь
- `POSTGRES_PASSWORD` - пароль

### Запуск через docker:
```sh
docker-compose up -d
```
Перед выполнением создайте файл переменных окружения (`.env`).\
Пример файла см. [Переменные среды](#Переменные-среды).

# Superhero Test Task

Тестовое задание

---

## Установка и запуск приложения

```bash
# Клонирование репозитория
git clone https://github.com/pavel-martyshev/SuperheroTestTask.git

# Переход в каталог проекта
cd SuperheroTestTask
```

Переименуйте файл .env.example в .env и заполните все поля.

```bash
# Сборка и запуск с помощью docker compose
sudo docker compose up --build 
```

---

## Описание работы

Поиск супергероя на `https://superheroapi.com/`. При успешном запросе к ресурсу, супергерой будет добавлен БД. Если в БД такой супергерой уже есть, то сервер вернет ответ со статусом `409 Conflict`. Если супергерой не будет найдет, то сервер вернет ответ со статусом `404 Not Found`.

```bash
curl -X POST http://localhost:8000/hero/ -H "Content-Type: application/json" -d '{"name": "Batman"}'
```

При выполнении GET-запроса без параметров, будут возвращены все супергерои из БД. Параметры без приставок `__lte` и `__gte` фильтруют супергероев по точному совпадению переданных значений. `__lte` - меньше или равно, `__gte` - больше или равно.

```bash
curl http://localhost:8000/hero/?name=intelligence=intelligence__gte=strength=strength__gte=strength__lte=speed=speed__gte=speed__lte=power=power__gte=power__lte=
```

---

## Тестирование
```bash
pytest
```
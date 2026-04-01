
## Базовый пример FastAPI + Aiosqlite c CRUD операциями

### Описание
- В примере представлены простые операции для работы с базой данных sqlite в асинхронном режиме.
- В менеджере сессий используется @asynccontextmanager - это гарантирует, что соединение с БД будет закрыто после завершения запроса.
- В примере не используется ORM и пул соединений.


### Тестирование api

**Добавить товар**
```shell
curl -X POST http://localhost:8000/items -H "Content-Type: application/json" -d '{"name":"Книга","price":12.99}'
curl -X POST http://localhost:8000/items -H "Content-Type: application/json" -d '{"name":"Fastapi","price":150.90}'
```

**Получить список товаров**
```shell
curl -X GET http://localhost:8000/items
```

**Получить товар по ID**
```shell
curl http://localhost:8000/items/1
```

**Обновить информацию о товаре**
```shell
curl -X PUT http://localhost:8000/items/1 -H "Content-Type: application/json" -d '{"name":"Книга (новая)","price":15.99}'
```

**Удалить товар**
```shell
curl -X DELETE http://localhost:8000/items/1
```

### Структура

```
./
├── app
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── routes
│   │   ├── api.py
│   │   └── frontend.py
│   ├── static
│   │   ├── css
│   │   │   └── default.css
│   │   ├── images
│   │   │   └── favicon.ico
│   │   └── js
│   │       └── default.js
│   └── templates
│       ├── 404.html
│       └── index.html
├── README.md
└── requirements.txt
```
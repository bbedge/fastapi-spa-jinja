
## Простой пример SPA на FastAPI + Jinja2Templates + Aiosqlite

### Описание
- Этот пример расширяет функционал [FastapiAiosqlite](https://github.com/bbedge/FastapiAiosqlite)  
- В примере реализована SPA с использованием JS и fetch.
- В примере используются стили w3cc и иконки Font Awesome Free 6.7.2.

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
│   │   │   ├── all.css
│   │   │   ├── all.min.css
│   │   │   ├── brands.css
│   │   │   ├── brands.min.css
│   │   │   ├── default.css
│   │   │   ├── fontawesome.css
│   │   │   ├── fontawesome.min.css
│   │   │   ├── regular.css
│   │   │   ├── regular.min.css
│   │   │   ├── solid.css
│   │   │   ├── solid.min.css
│   │   │   ├── svg-with-js.css
│   │   │   ├── svg-with-js.min.css
│   │   │   ├── v4-font-face.css
│   │   │   ├── v4-font-face.min.css
│   │   │   ├── v4-shims.css
│   │   │   ├── v4-shims.min.css
│   │   │   ├── v5-font-face.css
│   │   │   ├── v5-font-face.min.css
│   │   │   └── w3.css
│   │   ├── images
│   │   │   └── favicon.ico
│   │   ├── js
│   │   │   └── default.js
│   │   └── webfonts
│   │       ├── fa-brands-400.ttf
│   │       ├── fa-brands-400.woff2
│   │       ├── fa-regular-400.ttf
│   │       ├── fa-regular-400.woff2
│   │       ├── fa-solid-900.ttf
│   │       ├── fa-solid-900.woff2
│   │       ├── fa-v4compatibility.ttf
│   │       └── fa-v4compatibility.woff2
│   └── templates
│       ├── 404.html
│       └── index.html
├── database.sqlite
├── README.md
└── requirements.txt

```
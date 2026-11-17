# Simple start menu for TG bots

Готовый онбординг для aiogram 3: выбор языка → согласие с правилами → запись
пользователя в БД → главное меню. Плюс компактная админ-панель в том же боте.

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.32-2CA5E0?style=flat-square&logo=telegram&logoColor=white)](https://docs.aiogram.dev/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

## Что внутри

- **`/start`** — новый пользователь проходит выбор языка и согласие с правилами;
  повторный `/start` сразу ведёт в меню, без повторной регистрации.
- **4 языка** — `ru` / `en` / `es` / `ua`. Тексты лежат в JSON, а не в коде.
- **SQLite через `aiosqlite`** — `users.db` с таблицей `users`
  (`user_id`, `language`, `joinAT`); `log_admin.db` — журнал действий администратора.
- **Админ-панель** — статистика (всего пользователей, популярный язык, последняя
  регистрация), список пользователей, журнал действий, удаление пользователя.
- **Проверка доступа** — все админ-действия сверяют UID с переменной `admin` из `.env`.

## Структура

```text
.
├── config/
│   └── config_PG.py          # задел под PostgreSQL (сейчас не используется)
├── src/
│   ├── Start/                # онбординг: язык, правила, запись в БД
│   │   ├── start_menu.py     # хендлеры /start, язык, agree, restart
│   │   ├── start_keyboard.py # клавиатуры
│   │   ├── start_FSM.py      # состояния
│   │   └── start_language.json
│   ├── Menu/
│   │   ├── menu_main.py      # главное меню
│   │   ├── main_keyboard.py
│   │   └── menu_language.json
│   ├── Admin/                # админ-панель
│   │   ├── admin_menu.py
│   │   ├── admin_keyboard.py
│   │   └── admin_FSM.py
│   ├── SQL/
│   │   ├── start_SQL.py      # users: create / insert / get language
│   │   └── admin_SQL.py      # статистика, логи, удаление
│   └── main.py               # точка входа
├── .env.example
├── requirements.txt
└── README.md
```

## Быстрый старт

```bash
git clone https://github.com/WhyCrisis/Simple-start-menu-for-TG-bots.git
cd Simple-start-menu-for-TG-bots
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Windows PowerShell, если `cp` недоступен: `Copy-Item .env.example .env`.

### Переменные окружения

| Переменная | Зачем |
| :-- | :-- |
| `BOT_TOKEN` | токен от [@BotFather](https://t.me/BotFather) |
| `admin` | Telegram UID администратора — открывает доступ к админ-панели |
| `POSTGRES_*` | `HOST`, `PORT`, `USER`, `PASSWORD`, `DB` — задел под переезд на PostgreSQL, кодом пока не читаются |

Если `admin` пустой или нечисловой, админ-панель закрыта для всех — это безопасное
поведение по умолчанию.

### Запуск

```bash
# из корня репозитория
PYTHONPATH=src python -m src.main
```

```powershell
# Windows PowerShell
$env:PYTHONPATH = "src"; python -m src.main
```

> `PYTHONPATH=src` нужен, потому что в коде соседствуют импорты двух видов —
> `from src.Admin...` и `from SQL.start_SQL...`. Пока импорты не унифицированы,
> запуск возможен только из корня с этой переменной. Унификация — в Roadmap.

## Админ-панель

Открывается командой `/admin_menu_` и доступна только UID по из `.env`:

| Кнопка | Что делает |
| :-- | :-- |
| текущие пользователи | список UID, языка и даты регистрации |
| журнал действий | кто и что делал в админ-панели |
| удалить пользователя | запрос UID, подтверждение, удаление |


Каждое разрушительное действие пишется в `log_admin.db`.

## Кастомизация

| Что менять | Где |
| :-- | :-- |
| Тексты онбординга | `src/Start/start_language.json` |
| Текст главного меню | `src/Menu/menu_language.json` |
| Список языков | `choose_language()` в `start_keyboard.py` и фильтр в `start_menu.py` |
| Ссылки на правила | `rules_url` в `start_language.json` |

Тексты меню сейчас — заглушки («Main menu but english» и т. п.). Перед
использованием замените их на реальные: это то, что увидит пользователь.


## Лицензия

MIT — см. [LICENSE](LICENSE). Берите код, меняйте, используйте в своих проектах,
в том числе коммерческих; сохраняйте текст лицензии и указание авторства

## Автор

**Roman** — [@bartelliada](https://t.me/bartelliada) ·
[atomicsweetnes@gmail.com](mailto:atomicsweetnes@gmail.com) ·
[GitHub](https://github.com/WhyCrisis)

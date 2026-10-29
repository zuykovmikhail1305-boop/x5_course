# Сводка по городу

CLI-утилита: получает погоду (Open-Meteo) и курс валюты к рублю (Frankfurter), применяет правила предобработки и печатает сводку.

## Установка

Нужен Python 3.12+.

Через [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

Или через pip:

```bash
pip install requests
```

Зависимости: `requests` (см. `pyproject.toml`). API-ключи не нужны.

## Запуск

```bash
python main.py --city Moscow
```

```bash
python main.py --city Moscow --currency EUR
```

```bash
python main.py --city Moscow --json
```

При запуске через uv: `uv run python main.py --city Moscow`.

Аргументы:

- `--city` — название города (обязательно);
- `--currency` — ISO-код валюты, по умолчанию `USD`;
- `--json` — вывести сводку в формате JSON.

## Коды выхода

| Код | Значение |
|---|---|
| 0 | успех |
| 2 | ошибка аргументов |
| 3 | город или код валюты не найден |
| 4 | внешний сервис недоступен после повторов или вернул неожиданный ответ |

## Структура

- `clients/` — запросы к внешним API: timeout 10 с, 2 повтора при Timeout/ConnectionError/5xx, учёт `Retry-After` для 429, проверка ответов.
- `processing/` — правила предобработки (`preprocessing.py`) и сборка сводки (`service.py`).
- `main.py` — разбор аргументов, вывод и коды выхода.

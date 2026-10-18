# Участие в разработке

## Как предлагать идеи/фичи

Создайте Issue в репозитории с кратким описанием проблемы и желаемого поведения.

## Как предлагать код

Отправьте Pull Request с описанием изменений. До мержа убедитесь, что:

```bash
python -m pytest
ruff check .
```

- Код проходит тесты и линтер
- Описание PR содержит контекст: что было, что стало, зачем
- Новая фича = новый модуль в `dnsparse/` + тесты, а не разрастание
  существующих файлов

## Структура проекта

```
dns_parser.py          тонкая CLI-обёртка
dnsparse/
  __init__.py          экспорты: VERSION, DNSParser, DNSFormatter
  constants.py         VERSION
  core.py              DNSParser
  formatter.py         DNSFormatter
  cli.py               CLI (stdin/файлы, -o, --no-pretty, --gui)
  gui.py               GUI (Qt5/Qt6)
tests/                 юнит-тесты на синтетических данных
```

Направление зависимостей: `cli/gui -> core/formatter -> constants`.

## Конфиденциальность

Не прикладывайте реальные выгрузки с доменами клиентов в Issues/PR.

## Версионирование и релизы

- SemVer. Источник истины — `VERSION` в `dnsparse/constants.py`.
- Каждое изменение — запись в `CHANGELOG.md`.
- Релиз: обновить `VERSION` -> запись в CHANGELOG -> тег `vX.Y.Z`.
# Релизы

Процесс выпуска новой версии. Одинаков для всех модулей набора
Jealous Moon (`jealous-nginx`, `jealous-strace`, `jealous-domain`, `jealous-dns`).

## Версионирование

Semantic Versioning: `MAJOR.MINOR.PATCH`.

**Источник истины версии — `VERSION` в `dnsparse/constants.py`.**
`pyproject.toml` читает её автоматически через `[tool.setuptools.dynamic]`.

## Чек-лист релиза

1. Убедиться, что тесты и линтер зелёные:
   ```bash
   python -m pytest
   ruff check .
   ```
2. Обновить `VERSION` в `dnsparse/constants.py`
3. Добавить запись в `CHANGELOG.md`
4. Закоммитить: `git commit -m "Release vX.Y.Z"`
5. Поставить аннотированный тег: `git tag -a vX.Y.Z -m "jealous-dns X.Y.Z"`
6. Проверить сборку: `pip install .` и `jealous-dns --version`
7. Запушить вместе с тегом: `git push origin master --tags`
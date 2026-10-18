# Changelog

Все заметные изменения проекта документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
версионирование — [Semantic Versioning](https://semver.org/lang/ru/).

## [Unreleased]

## [0.1.0] — 2026-10-18

### Added
- Упаковка проекта: `pyproject.toml`, установка через `pip install jealous-dns`
  и консольная команда `jealous-dns`.
- Парсер DNS-выгрузок (`DNSParser`) и форматтер (`DNSFormatter`).
- CLI: stdin/файлы, `-o`, `--no-pretty`, `--gui`, gzip-вход.
- GUI на Qt5/Qt6 (`--gui`).
- Тесты на синтетических данных.
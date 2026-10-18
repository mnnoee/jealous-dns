# jealous-dns

[README in English](README.md)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

> Часть набора инструментов [Jealous Moon](https://github.com/mnnoee) —
> офлайн-диагностики серверов и доменов.

Парсер/форматтер DNS-записей: приводит «сырую» выгрузку хостинга/панели
к выровненному тексту. CLI + GUI (Qt5/Qt6).

## Установка

Пока не на PyPI (публикация планируется). Ставится напрямую с GitHub:

```bash
pip install git+https://github.com/mnnoee/jealous-dns.git
```

Для GUI дополнительно нужен PyQt5 или PyQt6:

```bash
pip install PyQt5   # или PyQt6
```

Можно запускать и без установки — прямо из клона репозитория:

```bash
python3 dns_parser.py /path/to/dump.txt
```

## Использование

```bash
jealous-dns dump.txt                  # вывод в stdout
jealous-dns dump.txt -o out.txt       # в файл
jealous-dns --no-pretty dump.txt      # без выравнивания
jealous-dns --gui                     # графический интерфейс
```

## Лицензия

GPL-3.0-or-later. См. [LICENSE](LICENSE) и [NOTICE](NOTICE).
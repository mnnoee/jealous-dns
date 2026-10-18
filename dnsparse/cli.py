"""CLI: чтение выгрузки, парсинг, форматирование, опциональный GUI."""

import argparse
import gzip
import os
import sys

from .constants import VERSION
from .core import DNSParser
from .formatter import DNSFormatter


def _open(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, encoding="utf-8", errors="replace")


def _read_inputs(paths):
    if not paths:
        return sys.stdin.read()
    chunks = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, fns in os.walk(p):
                for fn in sorted(fns):
                    fp = os.path.join(root, fn)
                    if os.path.isfile(fp):
                        with _open(fp) as f:
                            chunks.append(f.read())
        elif os.path.isfile(p):
            with _open(p) as f:
                chunks.append(f.read())
        else:
            print(f"Предупреждение: не найден путь {p}", file=sys.stderr)
    return "\n".join(chunks)


def main():
    ap = argparse.ArgumentParser(description="Парсер/форматтер DNS-записей (CLI + GUI)")
    ap.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    ap.add_argument("paths", nargs="*", help="файлы/каталоги с выгрузкой (по умолчанию stdin)")
    ap.add_argument("-o", "--output", help="файл для результата (по умолчанию stdout)")
    ap.add_argument("--no-pretty", action="store_true", help="не выравнивать колонки")
    ap.add_argument("--gui", action="store_true", help="запустить графический интерфейс (Qt5/6)")
    ap.add_argument("--json", nargs="?", const="report.json", metavar="PATH",
                    help="записать машиночитаемый JSON-отчёт (по умолчанию report.json)")
    args = ap.parse_args()

    if args.gui:
        from .gui import run_gui
        run_gui()
        return

    text = _read_inputs(args.paths)
    if not text.strip():
        print("Нет данных.", file=sys.stderr)
        # контракт --json: отчёт пишется даже когда распарсить нечего
        if args.json:
            from .json_export import write_json_report
            path = write_json_report([], args.json)
            print(f"JSON-отчёт записан в: {path}", file=sys.stderr)
        return

    records = DNSParser.parse(text)
    if not records:
        print("Не распознано. Проверь формат.", file=sys.stderr)
        # контракт --json: отчёт пишется даже когда распарсить нечего
        if args.json:
            from .json_export import write_json_report
            path = write_json_report([], args.json)
            print(f"JSON-отчёт записан в: {path}", file=sys.stderr)
        return

    formatted = DNSFormatter(is_pretty=not args.no_pretty).format(records)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(formatted + "\n")
        print(f"Результат записан в: {args.output}", file=sys.stderr)
    else:
        print(formatted)

    if args.json:
        from .json_export import write_json_report
        path = write_json_report(records, args.json)
        print(f"JSON-отчёт записан в: {path}", file=sys.stderr)


if __name__ == "__main__":
    main()

"""CLI: чтение выгрузки, парсинг, форматирование, опциональный GUI."""

import argparse
import gzip
import os
import shutil
import subprocess
import sys
import time

from .constants import VERSION
from .core import DNSParser
from .formatter import DNSFormatter
from .json_export import write_json_report


def _open(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, encoding="utf-8", errors="replace")


def _read_clipboard():
    """Прочитать текущее содержимое буфера обмена (или None при сбое).

    Мусор от браузера фильтруется в DNSParser.parse() (core.py, _clean_input).
    """
    for cmd in (
        ["xclip", "-selection", "clipboard", "-o"],
        ["xsel", "--clipboard", "--output"],
        ["wl-paste"],
    ):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            if out.returncode == 0:
                return out.stdout
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None


def _clipboard_available():
    """Есть ли в PATH хотя бы одна утилита чтения буфера обмена."""
    return any(shutil.which(cmd) for cmd in ("xclip", "xsel", "wl-paste"))


def _wait_for_new_clipboard(initial):
    """Ждать, пока в буфере появится новая запись (отличная от initial)."""
    print("Ожидание новой записи в буфере обмена (Ctrl+C для отмены)...", file=sys.stderr)
    try:
        while True:
            time.sleep(0.5)
            current = _read_clipboard()
            if current is None:
                continue
            if current != initial:
                print("Прочитано из буфера обмена.", file=sys.stderr)
                return current
    except KeyboardInterrupt:
        print("\nОтменено.", file=sys.stderr)
        return ""


def _read_inputs(paths):
    if not paths:
        if not sys.stdin.isatty():
            return sys.stdin.read()
        if not _clipboard_available():
            print("Буфер обмена недоступен. Вставь текст (Ctrl+D):", file=sys.stderr)
            return sys.stdin.read()
        initial = _read_clipboard()
        return _wait_for_new_clipboard(initial)
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
    ap.add_argument(
        "--json",
        nargs="?",
        const="report.json",
        metavar="PATH",
        help="записать машиночитаемый JSON-отчёт (по умолчанию report.json)",
    )
    args = ap.parse_args()

    if args.gui:
        from .gui import run_gui

        run_gui()
        return

    text = _read_inputs(args.paths)
    if not text.strip():
        print("Нет данных.", file=sys.stderr)
        print("Подсказка: передай файл/каталог или запусти с --gui.", file=sys.stderr)
        if args.json:
            path = write_json_report([], args.json)
            print(f"JSON-отчёт записан в: {path}", file=sys.stderr)
        return

    records = DNSParser.parse(text)
    if not records:
        print("Не распознано. Проверь формат.", file=sys.stderr)
        if args.json:
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
        path = write_json_report(records, args.json)
        print(f"JSON-отчёт записан в: {path}", file=sys.stderr)


if __name__ == "__main__":
    main()

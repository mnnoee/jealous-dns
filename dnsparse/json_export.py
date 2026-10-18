"""JSON-экспорт: машиночитаемый отчёт DNS-записей."""

import json
import os
from collections import Counter


def build_json(records):
    """Собирает dict со всеми результатами анализа."""
    by_type = Counter(r.get("type", "UNKNOWN") for r in records)
    return {
        "records": [
            {
                "name": r.get("name"),
                "type": r.get("type"),
                "value": r.get("value"),
                "priority": r.get("priority") or "",
            }
            for r in records
        ],
        "meta": {
            "total": len(records),
            "types": dict(by_type),
        },
    }


def write_json_report(records, path="report.json"):
    """Пишет JSON-отчёт в указанный путь, возвращает его."""
    doc = build_json(records)
    full = os.path.abspath(path)
    with open(full, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2, default=str)
    return full
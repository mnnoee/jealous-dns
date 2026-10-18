"""Ядро: парсинг «сырой» DNS-выгрузки (хостинг/панель) в список записей."""

import re


class DNSParser:
    """Превращает сырой текст выгрузки в список словарей записей."""

    @staticmethod
    def parse(text):
        lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
        records = []
        i = 0

        while i < len(lines):
            line = lines[i]
            if not line.endswith("."):
                i += 1
                continue

            name = line
            i += 1

            if i < len(lines) and re.fullmatch(r"\d+", lines[i]):
                i += 1

            if i >= len(lines):
                break

            typeline = lines[i]
            i += 1

            if "SOA" in typeline:
                while i < len(lines):
                    if lines[i].endswith(".") and i + 1 < len(lines) and re.fullmatch(r"\d+", lines[i + 1]):
                        break
                    i += 1
                continue

            record_type = ""
            if "MX" in typeline:
                record_type = "MX"
            elif "TXT" in typeline:
                record_type = "TXT"
            elif "A " in typeline or "(адрес" in typeline:
                record_type = "A"
            elif "NS" in typeline:
                record_type = "NS"
            else:
                record_type = typeline.split()[0] if typeline.split() else "UNKNOWN"

            value_lines = []
            priority = "10"

            while i < len(lines):
                current = lines[i]
                if current.endswith(".") and i + 1 < len(lines) and re.fullmatch(r"\d+", lines[i + 1]):
                    break

                if record_type == "MX" and "priority" in current.lower():
                    match = re.search(r"priority\s*=\s*(\d+)", current, re.IGNORECASE)
                    if match:
                        priority = match.group(1)
                else:
                    value_lines.append(current)

                i += 1

            value = " ".join(value_lines).strip()
            if not value:
                continue

            records.append({
                "name": name,
                "type": record_type,
                "value": value,
                "priority": priority if record_type == "MX" else "",
            })

        return records

"""Форматирование списка DNS-записей в текст."""

class DNSFormatter:
    """Форматирует записи в выровненный или простой текст."""

    def __init__(self, is_pretty=True):
        self.is_pretty = is_pretty

    def format(self, records):
        if not records:
            return ""

        output_lines = ["```"]
        processed = []
        for r in records:
            name = r["name"]
            rtype = r["type"]
            value = r["value"]
            if rtype == "MX":
                value = f"{value} (приоритет {r['priority']})"
            processed.append((name, rtype, value))

        if self.is_pretty:
            max_name = max(len(name) for name, _, _ in processed)
            max_type = max(len(rtype) for _, rtype, _ in processed)
            max_name = max(max_name, 25)
            max_type = max(max_type, 12)
            for name, rtype, value in processed:
                output_lines.append(f"{name.ljust(max_name)}\t{rtype.ljust(max_type)}\t{value}")
        else:
            for name, rtype, value in processed:
                output_lines.append(f"{name}\t{rtype}\t{value}")

        output_lines.append("```")
        return "\n".join(output_lines)

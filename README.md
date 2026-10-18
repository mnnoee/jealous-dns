# jealous-dns

> Part of the [Jealous Moon](https://github.com/mnnoee) toolkit — offline
> server and domain diagnostics.

DNS record parser/formatter: tidy hosting/panel dumps into aligned text.
CLI + Qt5/Qt6 GUI.

## Install

Not on PyPI yet (planned). Install straight from GitHub:

```bash
pip install git+https://github.com/mnnoee/jealous-dns.git
```

For the GUI, also install PyQt5 or PyQt6:

```bash
pip install PyQt5   # or PyQt6
```

Or run straight from a clone:

```bash
python3 dns_parser.py /path/to/dump.txt
```

## Usage

```bash
jealous-dns dump.txt                  # formatted to stdout
jealous-dns dump.txt -o out.txt       # to file
jealous-dns --no-pretty dump.txt      # compact
jealous-dns --gui                     # Qt GUI
```

## License

GPL-3.0-or-later.
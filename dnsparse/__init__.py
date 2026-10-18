"""dnsparse — модульный парсер/форматтер DNS-записей (CLI + GUI)."""

from .constants import VERSION
from .core import DNSParser
from .formatter import DNSFormatter

__version__ = VERSION

__all__ = ["VERSION", "__version__", "DNSParser", "DNSFormatter"]

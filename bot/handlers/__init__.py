# bot/handlers/__init__.py

from .start import handler as start
from .help import handler as help
from .watchlist import handler as watchlist
from .highest_volume import handler as highest_volume
from .lowest_closing import handler as lowest_closing
from .consolidated import handler as consolidated
from .nlp import handler as nlp
from .upload_csv import handler as upload_csv

__all__ = [
    "start",
    "help",
    "watchlist",
    "highest_volume",
    "lowest_closing",
    "consolidated",
    "nlp",
    "upload_csv",
]

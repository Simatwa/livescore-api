__version__ = "0.0.6"
__program__ = "livescore-api"
__repo__ = "https://github.com/Simatwa/livescore-api"
__info__ = "Access and manipulate matches from Livescore.com"
__author__ = "Smartwa"

from .main import json_formatter, livescore, utils
from .predictor import Make

__all__ = ["json_formatter", "livescore", "utils"]

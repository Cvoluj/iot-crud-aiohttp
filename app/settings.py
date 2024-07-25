import logging
import pathlib
from config import server_setting


BASE_DIR = pathlib.Path(__file__).parent.parent
LOG_LEVEL = server_setting.LOG_LEVEL
logging.basicConfig(level=logging.DEBUG)
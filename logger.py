# logger.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Diretório de logs
log_dir = "_logs"
os.makedirs(log_dir, exist_ok=True)

# Configura o logger principal
logger = logging.getLogger("LIENYX")
logger.setLevel(logging.DEBUG)

# Handler de rotação diária
file_handler = TimedRotatingFileHandler(
    filename=os.path.join(log_dir, "lienyx.log"),
    when="midnight",
    interval=1,
    backupCount=7,
    encoding='utf-8'
)
file_handler.setFormatter(logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))

# Stream para console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    "[%(levelname)s] %(message)s"
))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

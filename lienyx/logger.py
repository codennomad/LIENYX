from loguru import logger
import os
from pathlib import Path

# Diretório para logs
log_dir = Path("_logs")
log_dir.mkdir(exist_ok=True)

log_file = log_dir / "lienyx.log"

# Remove handlers padrão
logger.remove()

# Console bonito
logger.add(
    sink=lambda msg: print(msg, end=""),
    colorize=True,
    format="<cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan> | "
           "<level>{level: <8}</level> | "
           "<magenta>{name}</magenta>:<cyan>{function}</cyan> - "
           "<level>{message}</level>",
    level="DEBUG",
)

# Arquivo rotacionando
logger.add(
    str(log_file),
    rotation="00:00",      
    retention="7 days",    
    compression="zip",
    level="DEBUG",
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
)

# Adiciona nível 'SUCCESS' só se não existir
if not any(level.name == "SUCCESS" for level in logger._core.levels.values()):
    logger.level("SUCCESS", no=25, color="<green><bold>", icon="✔️")

def success(msg):
    logger.log("SUCCESS", msg)

logger.success = success

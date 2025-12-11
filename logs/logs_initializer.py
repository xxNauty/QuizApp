import logging

from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    filename=str(Path(__file__).resolve().parent) + f"/{datetime.now().strftime("%d_%m_%Y")}_logs.log",
    filemode='a',
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger('logs_initializer.py')

def init_logs() -> None:
    logs_path = str(Path(__file__).resolve().parent) + f"/{datetime.now().strftime("%d_%m_%Y")}_logs.log"
    try:
        open(logs_path, 'x').close()
        logger.info("Log file created")
    except FileExistsError:
        logger.info("Log file already exists")
        return
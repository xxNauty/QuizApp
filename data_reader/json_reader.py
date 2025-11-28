import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{datetime.now().strftime("%d_%m_%Y")}_logs.log",
    filemode='a',
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger("json_reader.py")

def read_file(filename: str, encoding: str = 'utf8') -> list[dict]|None:
    try:
        with open(filename, 'r', encoding=encoding) as file:
            questions = []

            data = json.load(file)
            for question in data:
                questions.append(question)

            logger.info("Questions read successfully from the %s file(JSON), there are %s questions", filename.split("/")[-1],  len(questions))
            file.close()
            return questions
    except FileNotFoundError:
        logger.error("There is no such file as %s", filename)
        return None
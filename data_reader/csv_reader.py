import csv
import logging

from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{datetime.now().strftime("%d_%m_%Y")}_logs.log",
    filemode='a',
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger("csv_reader.py")

def read_file(filename: str, encoding: str = 'utf8') -> list[dict]|None:
    try:
        with open(filename, 'r', encoding=encoding) as file:
            questions = []

            csv_file = csv.DictReader(file)
            for line in csv_file:
                questions.append(line)

            logger.info("Questions read successfully from the %s file(CSV), there are %s questions", filename.split("/")[-1],  len(questions))
            file.close()
            return questions
    except FileNotFoundError:
        logger.error("There is no such file as %s", filename)
        return None
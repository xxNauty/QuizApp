import csv
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
logger = logging.getLogger('data_reader.py')

def read_file(filename: str, file_format: str, encoding: str = 'utf8') -> list[dict]|None:
    try:
        with open(
                file=filename,
                mode='r',
                encoding=encoding
        ) as file:
            questions = []
            data_from_file = None

            match file_format:
                case "csv":
                    data_from_file = csv.DictReader(file)
                case 'json':
                    data_from_file = json.load(file)

            for question in data_from_file:
                question['id'] = int(question['id'])
                questions.append(question)

            logger.info("Questions read successfully from the %s file(%s), there are %s questions", filename.split("/")[-1], file_format.upper(),  len(questions))
            file.close()

            return questions
    except FileNotFoundError:
        logger.error("There is no such file as %s", filename.split("/")[-1])
        return None
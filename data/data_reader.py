import csv
import json
import logging

logging.basicConfig(level=logging.INFO)

def read_file(filename: str, data_format: str, encoding: str = 'utf8') -> list[dict]|None:
    try:
        with open(filename, 'r', encoding=encoding) as file:
            questions = []

            match data_format:
                case 'csv':
                    csv_file = csv.DictReader(file)
                    for line in csv_file:
                        questions.append(line)
                case 'json':
                    data = json.load(file)
                    for question in data:
                        questions.append(question)

            logging.info("Questions read successfully from the %s file(%s), there are %s questions", filename.split("/")[-1], data_format.upper(), len(questions))
            file.close()
            return questions
    except FileNotFoundError:
        logging.error("There is no such file as %s", filename)
        return None
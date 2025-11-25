import csv
import logging

logging.basicConfig(level=logging.INFO)

def read_file(filename: str, encoding: str = 'utf8') -> list[dict]|None:
    try:
        with open(filename, 'r', encoding=encoding) as file:
            questions = []

            csv_file = csv.DictReader(file)
            for line in csv_file:
                questions.append(line)

            logging.info("Questions read successfully from the %s file(CSV), there are %s questions", filename.split("/")[-1],  len(questions))
            file.close()
            return questions
    except FileNotFoundError:
        logging.error("There is no such file as %s", filename)
        return None
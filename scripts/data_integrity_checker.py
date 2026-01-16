import os
import sys
import yaml
import logging
import argparse

from datetime import datetime
from dotenv import load_dotenv
from database import data_reader

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    filename=f"scripts/script_logs/data_integrity_checker/{datetime.now().strftime("%Y_%m_%d")}_logs.log",
    filemode='a',
    format=os.getenv("LOGS_FORMAT"),
    encoding='utf-8'
)
logger = logging.getLogger("quiz_template_generator.py")

def verify(path_to_quiz: str) -> None:
    logger.info("----------------------------------------")
    logger.info(f"Verification of the quiz {path_to_quiz}")
    has_errors = False

    # sprawdzenie formatu pliku bazodanowego
    if os.path.exists(os.getenv("DATABASE_PATH") + path_to_quiz + "/data.json"):
        file_format = "json"
    elif os.path.exists(os.getenv("DATABASE_PATH") + path_to_quiz + "/data.csv"):
        file_format = "csv"
    else:
        logger.error("There is no such file, or file format is not supported")
        sys.exit()

    with open(os.getenv("DATABASE_PATH") + path_to_quiz + f"/data.{file_format}", 'r+', encoding="utf8") as file:
        lines_of_data = file.read().splitlines()

        # sprawdzenie czy liczba linii się zgadza
        if (len(lines_of_data) - 2) % 9 != 0:
            logger.error("Number of lines in database is wrong, something is missing")
            has_errors = True

        # sprawdzenie po kolei linii pliku
        number_of_line = 1
        while number_of_line < len(lines_of_data) - 1:
            if not lines_of_data[number_of_line] == "  {":
                logger.error(f"There is an error around line {number_of_line}")
                has_errors = True
                break
            number_of_line += 1

            if not lines_of_data[number_of_line].startswith('    "id"'):
                logger.error(f"There is an error around line {number_of_line}")
                has_errors = True
                break
            number_of_line += 1

            if not lines_of_data[number_of_line].startswith('    "question"'):
                logger.error(f"There is an error around line {number_of_line}")
                has_errors = True
                break
            number_of_line += 1

            if not lines_of_data[number_of_line].startswith('    "answer_a"'):
                logger.error(f"There is an error around line {number_of_line}")
                has_errors = True
                break
            number_of_line += 1

            if not lines_of_data[number_of_line].startswith('    "answer_b"'):
                logger.error(f"There is an error around line {number_of_line}")
                has_errors = True
                break
            number_of_line += 1

            if not lines_of_data[number_of_line].startswith('    "answer_c"'):
                logger.error(f"There is an error around line {number_of_line}")
                has_errors = True
                break
            number_of_line += 1

            if not lines_of_data[number_of_line].startswith('    "correct"'):
                logger.error(f"There is an error around line {number_of_line}")
                has_errors = True
                break
            number_of_line += 1

            if not lines_of_data[number_of_line].startswith('    "source"'):
                logger.error(f"There is an error around line {number_of_line}")
                has_errors = True
                break
            number_of_line += 1

            if number_of_line == len(lines_of_data) - 2:
                closing_bracket_line = "  }"
            else:
                closing_bracket_line = "  },"

            if not lines_of_data[number_of_line].startswith(closing_bracket_line):
                logger.error(f"There is an error around line {number_of_line}")
                has_errors = True
                break
            number_of_line += 1

        # sprawdzenie poprawności danych
        questions = data_reader.read_file(os.getenv("DATABASE_PATH") + path_to_quiz + f"/data.{file_format}", file_format="json", disable_logs=True)

        for question in questions:
            # sprawdzenie poprawności pola "correct"
            if "correct" in question and question['correct'] not in ["A", "B", "C"]:
                logger.error(f"There is an error with correct answer of question {question["id"]}")
                has_errors = True

        # sprawdzenie czy liczba pytań zgadza się z ilością linii w pliku
        if len(questions) != (len(lines_of_data) - 2) / 9:
            logger.error("Something is wrong with number of questions")
            has_errors = True

    if not has_errors:
        with open(os.getenv("DATABASE_PATH") + path_to_quiz + os.getenv("QUIZ_CONFIG_FILE"), 'r') as file:
            data_from_file = yaml.safe_load(file)
            file.close()
        data_from_file['integrity_verified'] = True

        with open(os.getenv("DATABASE_PATH") + path_to_quiz + os.getenv("QUIZ_CONFIG_FILE"), 'w') as file:
            yaml.dump(data_from_file, file, sort_keys=False)
            file.close()

        logger.info("Everything is ok with the database, marked as verified")
        print("Everything is ok with the database, marked as verified")
    else:
        logger.error("There are some errors with the database")
        print("There are some errors with the database. Check logs for detailed information")

    logger.info("----------------------------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify if database with question is complete and don't have any errors")
    parser.add_argument("path_to_quiz", type=str, help="Where is the quiz you want to verify")

    args = parser.parse_args()

    verify(args.path_to_quiz)
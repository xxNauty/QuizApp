import os
import logging

from datetime import datetime
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    filename=f"scripts/script_logs/quiz_template_generator/{datetime.now().strftime("%Y_%m_%d")}_logs.log",
    filemode='a',
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)
load_dotenv()

def generate() -> None:
    quiz_name = input("Name this quiz: ")
    quiz_name = quiz_name.lower().replace(" ", "_")

    database_format = ""
    correct_format = False
    while not correct_format:
        database_format = input("Chose format in which you want to store your questions (CSV/JSON): ")
        database_format = database_format.lower()

        if database_format in ['csv', 'json']:
            correct_format = True
        else:
            print("Only JSON and CSV are accepted")
            logger.error("Chosen incorrect database format")

    number_of_questions = input("Chose how many questions you want for single quiz: ")
    number_of_questions = int(number_of_questions)

    minimum_to_pass = 0
    correct_minimum_to_pass = False
    while not correct_minimum_to_pass:
        minimum_to_pass = input("Chose how many answers needs to be correct to pass the quiz: ")
        minimum_to_pass = int(minimum_to_pass)

        if minimum_to_pass <= number_of_questions:
            correct_minimum_to_pass = True
        else:
            print("This number cannot be greater than total number of questions in quiz")
            logger.error("Chosen higher min_to_pass than total number of questions")

    new_quiz_dir = os.getenv("DATASET_PATH") + quiz_name + "/"
    try:
        os.makedirs(new_quiz_dir)
    except OSError as error:
        logger.error(f"There was an error during the creation of the directory for new quiz: {error}")
    else:
        logger.info("Directory for quiz created successfully. Quiz data stored inside: %s", new_quiz_dir)

    try:
        with open(new_quiz_dir + os.getenv("QUIZ_CONFIG_FILE"), 'w') as file:
            file.write(f"quiz_name: {quiz_name}\n")
            file.write(f"number_of_questions: {number_of_questions}\n")
            file.write(f"minimum_to_pass: {minimum_to_pass}\n")
    except FileNotFoundError as error:
        logger.error(f"Directory not found, unable to create configuration file: {error}")
    except PermissionError as error:
        logger.error(f"Permission denied, cannot write to the configuration file: {error}")
    except TypeError as error:
        logger.error(f"{error}")
    except ValueError as error:
        logger.error(f"{error}")
    except OSError as error:
        logger.error(f"{error}")
    except Exception as error:
        logger.error(f"An unexpected error happened: {error}")
    else:
        logger.info("Configuration file created and filled with data")

    try:
        with open(new_quiz_dir + os.getenv("DATABASE_FILE_NAME") + database_format, 'w'):
            pass
    except FileNotFoundError as error:
        logger.error(f"Directory not found, unable to create dataset file: {error}")
    except TypeError as error:
        logger.error(f"{error}")
    except ValueError as error:
        logger.error(f"{error}")
    except OSError as error:
        logger.error(f"{error}")
    except Exception as error:
        logger.error(f"An unexpected error happened: {error}")
    else:
        logger.info("Database for questions created")

if __name__ == "__main__":
    generate()
import os
import logging

from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    filename=f"script_logs/quiz_template_generator/{datetime.now().strftime("%d_%m_%Y")}_logs.log",
    filemode='a',
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger("quiz_template_generator.py")

def generate() -> None:
    quiz_name = input("Name this quiz: ")
    quiz_name = quiz_name.lower().replace(" ", "-")

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

    new_quiz_dir = "database/" + quiz_name + "/"
    os.makedirs(new_quiz_dir) # katalog utworzony
    logger.info("Directory for quiz created successfully. Quiz data stored inside: %s", new_quiz_dir)

    # plik konfiguracyjny utworzony
    with open(new_quiz_dir + "config.yaml", 'w') as file:
        logger.info("Configuration file created")

        file.write(f"quiz_name: {quiz_name}\n")
        file.write(f"number_of_questions: {number_of_questions}\n")
        file.write(f"minimum_to_pass: {minimum_to_pass}\n")
        file.write("integrity_verified: false")

        logger.info("Configuration file filled with data")

        file.close()

    # utworzenie pustego pliku dla bazy pytań
    with open(new_quiz_dir + "data." + database_format, 'w') as file:
        logger.info("Database for questions created")
        file.close()

if __name__ == "__main__":
    generate()
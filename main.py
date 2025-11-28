import os.path

import yaml
import logging
import quiz_generator

from data import data_reader
from data_reader import csv_reader, json_reader
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{datetime.now().strftime("%d_%m_%Y")}_logs.log",
    filemode='a',
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger("main.py")

def read_configuration_of_quiz(directory_of_data) -> tuple[int, int, str]:
    try:
        with open(directory_of_data + "config.yaml") as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)
            quiz_name = data['quiz_name']
            number_of_questions = data['number_of_questions']
            minimum_to_pass = data['minimum_to_pass']
            logger.info("Configuration read from config.yaml file.")

            file.close()
    except FileNotFoundError:
        print("There is no file with configuration. You have to pass the settings now")

        quiz_name = "No title for quiz"
        number_of_questions = int(input("How many questions should the test have?"))
        minimum_to_pass = int(input("How many answers have to be correct in order to pass?"))
        logger.info("Configuration file not found, read from user input")

    return number_of_questions, minimum_to_pass, quiz_name

def read_question_database(directory_of_data) -> list|None:
    if os.path.exists(directory_of_data + "data.json"):
        questions = json_reader.read_file(directory_of_data + "data.json")
    elif os.path.exists(directory_of_data + "data.csv"):
        questions = csv_reader.read_file(directory_of_data + "data.csv")
    else:
        logger.error("There is no file with questions")
        return None
    return questions

def play(directory_of_data: str) -> None:
    number_of_questions, minimum_to_pass, quiz_name = read_configuration_of_quiz(directory_of_data)
    questions = read_question_database(directory_of_data)
    quiz = quiz_generator.generate_quiz(questions, number_of_questions) # losowanie pytań do quizu

    logger.info("----Game Starts----")
    logger.info(f"Topic of the quiz: {quiz_name}")

    answers = []
    correct_answers = 0
    print("The quiz starts")
    for i in range(number_of_questions):
        print(f"\nQuestion number {i + 1}:")
        print(quiz[i]['PYTANIE'])
        print("a) " + quiz[i]['ODP_A'])
        print("b) " + quiz[i]['ODP_B'])
        print("c) " + quiz[i]['ODP_C'])
        print()

        choice = input("Choose correct answer (a/b/c):")
        chosen_answer = ''
        match choice.lower():
            case 'a':
                chosen_answer = quiz[i]['ODP_A']
            case 'b':
                chosen_answer = quiz[i]['ODP_B']
            case 'c':
                chosen_answer = quiz[i]['ODP_C']

        correct_answer = ''
        match quiz[i]['POPRAWNA']:
            case 'A':
                correct_answer = quiz[i]['ODP_A']
            case 'B':
                correct_answer = quiz[i]['ODP_B']
            case 'C':
                correct_answer = quiz[i]['ODP_C']

        answers.append((quiz[i]['PYTANIE'], chosen_answer, choice.upper() == quiz[i]['POPRAWNA'], correct_answer))
        if choice.upper() == quiz[i]['POPRAWNA']:
            correct_answers += 1

    logger.info("Quiz ended")

    if correct_answers >= minimum_to_pass:
        print(f"Congratulations! You passed!({correct_answers}/{number_of_questions})\nHere are your results:")
        logger.info(f"Test passed({correct_answers}/{number_of_questions})")
    else:
        print(f"You failed, your score is {correct_answers}/{number_of_questions}. You need to have at least {minimum_to_pass} correct answers to pass")
        logger.info(f"Test failed({correct_answers}/{number_of_questions})")

    for i, single_result in enumerate(answers):
        question, chosen_answer, is_correct, correct_answer = single_result
        print(f"Question number {i}: {question}")
        print(f"Your choice: {chosen_answer}")
        if is_correct:
            print("Your answer is correct!")
        else:
            print(f"Correct answer: {correct_answer}")

if __name__ == "__main__":
    play("data/pozwolenie-na-posiadanie-broni-palnej/")
import sys

import yaml
import logging

from os import path
from datetime import datetime
from database import data_reader, quiz_generator

logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{datetime.now().strftime("%d_%m_%Y")}_logs.log",
    filemode='a',
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger("main.py")

def read_configuration_of_quiz(directory_of_data, number_of_questions_in_database) -> tuple[int, int, str]:
    try:
        with open(directory_of_data + "config.yaml") as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)
            quiz_name = data['quiz_name']
            number_of_questions = data['number_of_questions']
            minimum_to_pass = data['minimum_to_pass']
            logger.info("Configuration read from config.yaml file.")
            logger.info(f"Topic of the quiz: {quiz_name}")

            file.close()
        return number_of_questions, minimum_to_pass, quiz_name

    except FileNotFoundError:
        print("There is no file with configuration. You have to pass the settings now")

        quiz_name = "No title for quiz"

        logger.info("Configuration file not found, read from user input")
        logger.info(f"Topic of the quiz: {quiz_name}")

        correct_number_of_questions = False
        number_of_questions = 0
        while not correct_number_of_questions:
            number_of_questions = int(input("How many questions should the test have?"))
            if number_of_questions <= number_of_questions_in_database:
                correct_number_of_questions = True
            else:
                print(f"There is not enough questions in database to form such long quiz, choose number smaller than or equal to {number_of_questions_in_database}")
                logger.error("Incorrect number of questions per quiz value")

        correct_min_to_pass = False
        minimum_to_pass = 0
        while not correct_min_to_pass:
            minimum_to_pass = int(input("How many answers have to be correct in order to pass?"))
            if minimum_to_pass <= number_of_questions:
                correct_min_to_pass = True
            else:
                print(f"You cannot set minimum to pass to higher number than total number of questions in quiz({number_of_questions})")
                logger.error("Incorrect min_to_pass value")

        return number_of_questions, minimum_to_pass, quiz_name

def read_question_database(directory_of_data) -> list|None:
    if path.exists(directory_of_data + "data.json"):
        questions = data_reader.read_file(directory_of_data + "data.json", 'json')
        logger.info("Questions read from the JSON file")
    elif path.exists(directory_of_data + "data.csv"):
        questions = data_reader.read_file(directory_of_data + "data.json", 'csv')
        logger.info("Questions read from the CSV file")
    else:
        logger.error("There is no file with questions")
        return None
    return questions

def play(directory_of_data: str) -> None:
    questions = read_question_database(directory_of_data)
    number_of_questions, minimum_to_pass, quiz_name = read_configuration_of_quiz(directory_of_data, len(questions))
    quiz = quiz_generator.generate_quiz(questions, number_of_questions) # losowanie pytań do quizu

    logger.info("----Game Starts----")

    answers = []
    correct_answers = 0
    print("The quiz starts")
    for i in range(number_of_questions):
        print(f"\nQuestion number {i + 1}:")
        print(quiz[i]['question'])
        print("a) " + quiz[i]['answer_a'])
        print("b) " + quiz[i]['answer_b'])
        print("c) " + quiz[i]['answer_c'])
        print()

        choice = input("Choose correct answer (a/b/c):")
        chosen_answer = ''
        match choice.lower():
            case 'a':
                chosen_answer = quiz[i]['answer_a']
            case 'b':
                chosen_answer = quiz[i]['answer_b']
            case 'c':
                chosen_answer = quiz[i]['answer_c']

        correct_answer = ''
        match quiz[i]['correct']:
            case 'A':
                correct_answer = quiz[i]['answer_a']
            case 'B':
                correct_answer = quiz[i]['answer_b']
            case 'C':
                correct_answer = quiz[i]['answer_c']

        answers.append((quiz[i]['question'], chosen_answer, choice.upper() == quiz[i]['correct'], correct_answer))
        logger.info(f"For question number {i + 1} user chose answer |{choice}|. It's {"Correct" if choice.upper() == quiz[i]['correct'] else "Wrong"}!")
        if choice.upper() == quiz[i]['correct']:
            correct_answers += 1

    logger.info("Quiz ended")

    if correct_answers >= minimum_to_pass:
        print(f"Congratulations! You passed!({correct_answers}/{number_of_questions})\nHere are your results:")
        logger.info(f"Test passed({correct_answers}/{number_of_questions})")
    else:
        print(f"You failed, your score is {correct_answers}/{number_of_questions}. You need to have at least {minimum_to_pass} correct answers to pass\nHere are your results:")
        logger.info(f"Test failed({correct_answers}/{number_of_questions})")

    for i, single_result in enumerate(answers):
        question, chosen_answer, is_correct, correct_answer = single_result
        print(f"\nQuestion number {i + 1}: {question}")
        print(f"Your choice: \n\t{chosen_answer}")
        if is_correct:
            print("Your answer is correct!")
        else:
            print(f"Correct answer: \n\t{correct_answer}")

if __name__ == "__main__":
    logger.info("-------------------------------------")
    play("database/pozwolenie-na-bron/")
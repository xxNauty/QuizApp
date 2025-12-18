import sys
import yaml
import logging
import argparse

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

def read_configuration_of_quiz(directory_of_data) -> tuple[int, int, str, bool]:
    with open(directory_of_data + "config.yaml") as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
        quiz_name = data['quiz_name']
        number_of_questions = data['number_of_questions']
        minimum_to_pass = data['minimum_to_pass']
        verified = bool(data['integrity_verified'])

        logger.info("Configuration read from config.yaml file.")
        logger.info(f"Topic of the quiz: {quiz_name}")

        file.close()
    return number_of_questions, minimum_to_pass, quiz_name, verified

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
    directory_of_data = "database/" + directory_of_data + "/"
    questions = read_question_database(directory_of_data)
    number_of_questions, minimum_to_pass, quiz_name, verified = read_configuration_of_quiz(directory_of_data)

    if not verified:
        print("You cannot use unverified database for quiz, check it's integrity before using.")
        logger.error("Attempt to use unverified database")
        sys.exit()

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
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_quiz", type=str)

    args = parser.parse_args()

    logger.info("-------------------------------------")
    play(args.path_to_quiz)
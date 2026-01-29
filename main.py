import os
import yaml
import logging
import argparse

from datetime import datetime
from dotenv import load_dotenv
from database import data_reader

from quiz_generator import generate_quiz
from update_statistics import update_statistics_for_question


logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{datetime.now().strftime("%Y_%m_%d")}_logs.log",
    filemode='a',
    format=os.getenv("LOGS_FORMAT"),
    encoding='utf-8'
)
logger = logging.getLogger(__name__)
load_dotenv()

def read_configuration_of_quiz(directory_of_data) -> tuple[int, int, str]:
    with open(directory_of_data + os.getenv("QUIZ_CONFIG_FILE")) as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
        quiz_name = data['quiz_name']
        number_of_questions = data['number_of_questions']
        minimum_to_pass = data['minimum_to_pass']

        logger.info("Configuration read from config.yaml file.")
        logger.info(f"Topic of the quiz: {quiz_name}")

        file.close()
    return number_of_questions, minimum_to_pass, quiz_name

def play(directory_of_data: str) -> None:
    directory_of_data = os.getenv("DATASET_PATH") + directory_of_data + "/"
    number_of_questions, minimum_to_pass, quiz_name = read_configuration_of_quiz(directory_of_data)
    questions = data_reader.read_database(quiz_name)

    quiz = generate_quiz(questions, number_of_questions) # choosing questions for quiz

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

        answers.append((quiz[i]['question'], chosen_answer, choice.upper() == quiz[i]['correct'], correct_answer, quiz[i]['id']))
        logger.info(f"For question number {i + 1} user chose answer |{choice}|. It's {"Correct" if choice.upper() == quiz[i]['correct'] else "Wrong"}!")
        if choice.upper() == quiz[i]['correct']:
            correct_answers += 1

    logger.info("Quiz ended")

    print("\nHere are your results:")
    wrong_answers = []
    for i, single_result in enumerate(answers):
        question, chosen_answer, is_correct, correct_answer, question_id = single_result
        update_statistics_for_question(quiz_name, question_id, is_correct)
        if not is_correct:
            wrong_answers.append(i + 1)
            print(f"\nQuestion number {i + 1}: {question}")
            print(f"Your choice: \n\t{chosen_answer}")
            print(f"Correct answer: \n\t{correct_answer}")

    print("\n------------------------------")
    if correct_answers >= minimum_to_pass:
        print(f"Congratulations! You passed!({correct_answers}/{number_of_questions})")
        logger.info(f"Test passed({correct_answers}/{number_of_questions})")
    else:
        print(f"You failed({correct_answers}/{number_of_questions}).\nYou need to have at least {minimum_to_pass} correct answers to pass")
        logger.info(f"Test failed({correct_answers}/{number_of_questions})")

    if len(wrong_answers) > 0:
        print("Wrong answers in questions number:\n\t", ", ".join(map(str, wrong_answers)))
    print("------------------------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_quiz", type=str)

    args = parser.parse_args()

    logger.info("-------------------------------------")
    play(args.path_to_quiz)
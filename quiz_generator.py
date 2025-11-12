import random
import logging

def generate_quiz(available_questions: list, number_of_questions) -> list[dict]:
    if type(available_questions) is not list:
        raise TypeError(f"Quiz can be generated only from list of questions, not {type(available_questions)}")

    ids_of_questions = set()
    while len(ids_of_questions) < number_of_questions:
        ids_of_questions.add(random.randint(0, len(available_questions) - 1))

    questions = []
    logging.info("The question drawing begins")
    for id_of_questions in ids_of_questions:
        logging.info(f"Chosen question number {id_of_questions + 1}")
        questions.append(available_questions[id_of_questions])

    logging.info(f"Quiz generated, there are {number_of_questions} questions")

    return questions
import random
import logging

logger = logging.getLogger("quiz_generator.py")

def generate_quiz(available_questions: list, number_of_questions: int) -> list[dict]|None:
    ids_of_questions = set()

    if len(available_questions) < number_of_questions:
        logger.error("There is not enough questions in database to form such long quiz")
        return None

    while len(ids_of_questions) < number_of_questions:
        ids_of_questions.add(random.randint(0, len(available_questions) - 1))

    questions = []

    logger.info("The question drawing begins")
    for id_of_questions in ids_of_questions:
        logger.info(f"Chosen question number {id_of_questions + 1}")
        questions.append(available_questions[id_of_questions])

    logger.info(f"Quiz generated, there are {number_of_questions} questions")

    return questions
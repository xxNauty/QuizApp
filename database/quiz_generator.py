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
        questions.append(_shuffle_answers(available_questions[id_of_questions]))

    logger.info(f"Quiz generated, there are {number_of_questions} questions")

    return questions

def _shuffle_answers(question: dict) -> dict:
    letters_of_answers = ['A', 'B', 'C']
    answers = [
        ["A", question['answer_a']],
        ["B", question['answer_b']],
        ["C", question['answer_c']]
    ]
    random.shuffle(answers)

    question['answer_a'] = answers[0][1]
    question['answer_b'] = answers[1][1]
    question['answer_c'] = answers[2][1]

    for i in range(3):
        if answers[i][0] == question['correct']:
            question['correct'] = letters_of_answers[i]
            break

    return question
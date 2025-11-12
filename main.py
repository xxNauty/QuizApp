import os.path

import yaml
import logging
import quiz_generator

from data_reader import csv_reader, json_reader

DIRECTORY_OF_DATA = "data/pozwolenie-na-posiadanie-broni-palnej/"

def read_configuration_of_quiz() -> tuple[int, int]:
    try:
        with open(DIRECTORY_OF_DATA + "config.yaml") as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)
            number_of_questions = data['number_of_questions']
            minimum_to_pass = data['minimum_to_pass']
            # number_of_questions = 5
            # minimum_to_pass = 3

            file.close()
    except FileNotFoundError:
        logging.error("There is no file with configuration. You have to pass the settings now")

        number_of_questions = int(input("How many questions should the test have?"))
        minimum_to_pass = int(input("How many answers have to be correct in order to pass?"))

    return number_of_questions, minimum_to_pass

def read_question_database() -> list|None:
    if os.path.exists(DIRECTORY_OF_DATA + "data.json"):
        questions = json_reader.read_file(DIRECTORY_OF_DATA + "data.json")
    elif os.path.exists(DIRECTORY_OF_DATA + "data.csv"):
        questions = csv_reader.read_file(DIRECTORY_OF_DATA + "data.csv")
    else:
        logging.error("There is no file with questions")
        return None
    return questions

def play():
    number_of_questions, minimum_to_pass = read_configuration_of_quiz()
    questions = read_question_database()
    quiz = quiz_generator.generate(questions, number_of_questions) # losowanie pytań do quizu

    answers = []
    correct_answers = 0
    print("The quiz starts")
    for i in range(number_of_questions):
        print(f"Question number {i + 1}:")
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

    if correct_answers >= minimum_to_pass:
        print(f"Congratulations! You passed!({correct_answers}/{number_of_questions})\nHere are your results:")
    else:
        print(f"You failed, your score is {correct_answers}/{number_of_questions}. You need to have at least {minimum_to_pass} correct answers to pass")

    for i, single_result in enumerate(answers):
        question, chosen_answer, is_correct, correct_answer = single_result
        print(f"Question number {i}: {question}")
        print(f"Your choice: {chosen_answer}")
        if is_correct:
            print("Your answer is correct!")
        else:
            print(f"Correct answer: {correct_answer}")

play()
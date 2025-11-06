import os.path

import yaml
import logging
import quiz_generator

from data_reader import csv_reader, json_reader

DIRECTORY_OF_DATA = "data/pozwolenie-na-posiadanie-broni-palnej/"

def play():
    # odczytywanie pliku z konfiguracją quizu
    try:
        with open(DIRECTORY_OF_DATA + "config.yaml") as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)
            number_of_questions = data['number_of_questions']
            minimum_to_pass = data['minimum_to_pass']
            # wartości na czas testów
            # number_of_questions = 5
            # minimum_to_pass = 3
            file.close()
    except FileNotFoundError:
        logging.error("There is no file with configuration. You have to pass the settings now")
        number_of_questions = int(input("How many questions should the test have?"))
        minimum_to_pass = int(input("How many answers have to be correct in order to pass?"))

    # sprawdzanie formatu pliku wejściowego
    if os.path.exists(DIRECTORY_OF_DATA + "data.json"):
        questions = json_reader.read_file(DIRECTORY_OF_DATA + "data.json")
    elif os.path.exists(DIRECTORY_OF_DATA + "data.csv"):
        questions = csv_reader.read_file(DIRECTORY_OF_DATA + "data.csv")
    else:
        logging.error("There is no file with questions")
        return

    # losowanie pytań do quizu
    quiz = quiz_generator.generate(questions, number_of_questions)

    # gra rozpoczyna się

    score = []
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
        score.append((quiz[i]['PYTANIE'], choice, choice.upper() == quiz[i]['POPRAWNA'], quiz[i]['POPRAWNA']))
        if choice.upper() == quiz[i]['POPRAWNA']:
            correct_answers += 1

    if correct_answers >= minimum_to_pass:
        print("Congratulations! You passed!\nHere are your results:")

    for i, single_result in enumerate(score):
        question, choice, is_correct, correct = single_result
        print(f"Question number {i}: {question}")
        print(f"Your choice: {choice}")
        if is_correct:
            print("Your answer is correct!")
        else:
            print(f"Correct answer: {correct}")

play()
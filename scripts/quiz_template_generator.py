import os

def generate(custom_quiz_dir = ""):
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

    new_quiz_dir = "../data/" + quiz_name + "/" if custom_quiz_dir == "" else custom_quiz_dir + quiz_name + "/"
    os.makedirs(new_quiz_dir) # katalog utworzony

    # plik konfiguracyjny utworzony
    with open(new_quiz_dir + "config.yaml", 'w') as file:
        file.write(f"number_of_questions: {number_of_questions}\n")
        file.write(f"minimum_to_pass: {minimum_to_pass}\n")
        file.close()

    # utworzenie pustego pliku dla bazy pytań
    with open(new_quiz_dir + "data." + database_format, 'w') as file:
        file.close()

if __name__ == "__main__":
    generate()
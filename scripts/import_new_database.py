import csv
import json
import sqlite3
import logging
import argparse

from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    filename=f"scripts/script_logs/import_new_database/{datetime.now().strftime("%Y_%m_%d")}_logs.log",
    filemode='a',
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger("import_new_database.py")

def import_database(name_of_quiz: str, format_of_dataset:str):
    working_dir = f"database/{name_of_quiz}/"
    name_of_quiz = name_of_quiz.replace("-", "_")
    database_connection = sqlite3.connect("database/database.db")
    cursor = database_connection.cursor()

    #check if table for questions already exists
    cursor.execute(f"SELECT 1 FROM sqlite_master WHERE type='table' AND name='{name_of_quiz}'")
    questions_table_exists = cursor.fetchone() is not None

    if not questions_table_exists:
        logging.info("Creating table for questions")

    #create table for questions
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {name_of_quiz} (
            id INT PRIMARY KEY,
            question VARCHAR(255) NOT NULL,
            answer_a VARCHAR(255) NOT NULL,
            answer_b VARCHAR(255) NOT NULL,
            answer_c VARCHAR(255) NOT NULL,
            correct VARCHAR(255) NOT NULL,
            source VARCHAR(255) NOT NULL
        )
    """)

    # check if table for statistics already exists
    cursor.execute(f"SELECT 1 FROM sqlite_master WHERE type='table' AND name='{name_of_quiz}_statistics'")
    questions_table_exists = cursor.fetchone() is not None

    if not questions_table_exists:
        logging.info("Creating table for statistics")

    #create table for question statistics
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {name_of_quiz}_statistics (
            question_id INT PRIMARY KEY,
            times_chosen INT NOT NULL,
            times_correct INT NOT NULL
        )
    """)

    with open(f"{working_dir}data.{format_of_dataset.lower()}", 'r', encoding='utf-8') as file:
        match format_of_dataset:
            case "CSV":
                data_from_file = csv.DictReader(file)
            case 'JSON':
                data_from_file = json.load(file)

        for question in data_from_file:
            question['id'] = int(question['id'])

            #add question to questions database,
            #when question is already there check if is the similar to the one in question variable,
            #if not do update
            cursor.execute(f"""
                INSERT INTO {name_of_quiz} VALUES 
                (
                    {question['id']},
                    '{question['question']}',
                    '{question['answer_a']}',
                    '{question['answer_b']}',
                    '{question['answer_c']}',
                    '{question['correct']}',
                    '{question['source']}'
                )
                ON CONFLICT (id) DO UPDATE
                SET
                question = '{question['question']}',
                answer_a = '{question['answer_a']}',
                answer_b = '{question['answer_b']}',
                answer_c = '{question['answer_c']}',
                correct = '{question['correct']}',
                source = '{question['source']}'
                WHERE 
                (
                    {name_of_quiz}.question,
                    {name_of_quiz}.answer_a,
                    {name_of_quiz}.answer_b,
                    {name_of_quiz}.answer_c,
                    {name_of_quiz}.correct,
                    {name_of_quiz}.source
                )
                IS DISTINCT FROM
                (
                    '{question['question']}',
                    '{question['answer_a']}',
                    '{question['answer_b']}',
                    '{question['answer_c']}',
                    '{question['correct']}',
                    '{question['source']}'
                )
            """)

            # 1) how many rows changed by the last statement
            changed = database_connection.execute("SELECT changes()").fetchone()[0]

            if changed == 0:
                pass
            else:
                last_id = cursor.lastrowid
                if last_id is not None and last_id != 0:
                    logging.info(f"Inserted new question: {question['question']}")
                    # add row for question's statistics
                    cursor.execute(f"""
                        INSERT INTO {name_of_quiz}_statistics VALUES (
                            {question['id']},
                            0,
                            0
                        )
                    """)
                else:
                    logging.info(f"Question number {question['id']} updated")
                    #clear statistics for updated question
                    cursor.execute(f"""
                        UPDATE {name_of_quiz}_statistics
                        SET times_chosen=0, times_correct=0
                        WHERE question_id LIKE {question['id']}
                    """)

            database_connection.commit()

        file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import new set of questions into database")
    parser.add_argument("path_to_dataset", type=str, help="Path to folder with dataset of questions")
    parser.add_argument("format_of_dataset", type=str, help="In which format is the dataset (CSV/JSON)")

    args = parser.parse_args()

    import_database(args.path_to_dataset, args.format_of_dataset)

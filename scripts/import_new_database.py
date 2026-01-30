import os
import csv
import sys
import json
import sqlite3
import logging
import argparse

from datetime import datetime
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    filename=os.getenv("LOGS_PATH") + datetime.now().strftime("%Y_%m_%d") + ".log",
    filemode='a',
    format=os.getenv("LOGS_FORMAT"),
    encoding='utf-8'
)
logger = logging.getLogger("script")
load_dotenv()

def validate_inputs(quiz_name: str, format_of_dataset: str) -> None:
    try:
        if not isinstance(quiz_name, str) or not quiz_name.isidentifier():
            raise ValueError("Invalid name of quiz provided")
        if not isinstance(format_of_dataset, str) or format_of_dataset not in ['json', 'csv']:  # in future also PDF
            raise ValueError("Invalid or not supported format of dataset")
    except ValueError as error:
        logger.critical(f"There was an error with the input parameters: {error}")
        sys.exit()
    except Exception as error:
        logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")

def create_tables(quiz_name: str, cursor: sqlite3.Cursor) -> None:
    # create table for questions
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {quiz_name} (
                id INT PRIMARY KEY,
                question VARCHAR(255) NOT NULL,
                answer_a VARCHAR(255) NOT NULL,
                answer_b VARCHAR(255) NOT NULL,
                answer_c VARCHAR(255) NOT NULL,
                correct VARCHAR(255) NOT NULL,
                source VARCHAR(255) NOT NULL
            )
        """)
    except sqlite3.DatabaseError as error:
        logger.error(f"There was an error during the creation of the question table: {error}")
        sys.exit()
    except Exception as error:
        logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")
    else:
        logger.info("Database for question created successfully or already exist")  # TODO: log this two options separately

    # create table for question statistics
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {quiz_name}_statistics (
                question_id INT PRIMARY KEY,
                times_chosen INT NOT NULL,
                times_correct INT NOT NULL
            )
        """)
    except sqlite3.DatabaseError as error:
        logger.error(f"There was an error during the creation of the statistics table: {error}")
        sys.exit()
    except Exception as error:
        logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")
    else:
        logger.info("Database for question created successfully or already exist")  # TODO: log this two options separately

def read_file(quiz_name: str, format_of_dataset: str) -> list[dict] | None:
    data_from_file = []
    try:
        with open(f"database/{quiz_name}/data.{format_of_dataset}", 'r', encoding='utf-8') as file:
            match format_of_dataset:
                case "csv":
                    data_from_file = csv.DictReader(file)
                case 'json':
                    data_from_file = json.load(file)
    # handle file errors
    except FileNotFoundError as error:
        logger.error(f"There is no file with questions in given directory: {error}")
        sys.exit()
    except PermissionError as error:
        logger.critical(f"The code cannot access file with questions because of the permission error: {error}")
        sys.exit()
    except IsADirectoryError as error:
        logger.critical(f"Given path leads to a directory, not a file: {error}")
        sys.exit()
    except UnicodeError as error:
        logger.error(f"File encoding must be UTF-8: {error}")
        sys.exit()
    # handle csv error
    except csv.Error as error:
        logger.error(f"There was an error while processing CSV file: {error}")
        sys.exit()
    # handle json error
    except json.JSONDecodeError as error:
        logger.error(f"There was an error while processing JSON file: {error}")
        sys.exit()
    except Exception as error:
        logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")
    else:
        logger.info("Questions from the file read successfully")
        return data_from_file

def insert_question(question: dict, quiz_name: str, cursor: sqlite3.Cursor) -> None:
    question['id'] = int(question['id'])

    # add question to questions database,
    # when question is already there check if is the similar to the one in question variable,
    # if not do update
    insert_query = f"""
        INSERT INTO {quiz_name} VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (id) DO UPDATE SET
        question = excluded.question,
        answer_a = excluded.answer.a,
        answer_b = excluded.answer.b,
        answer_c = excluded.answer.c,
        correct = excluded.correct,
        source = excluded.source,
    """
    insert_params = (
        question['id'],
        question['question'],
        question['answer_a'],
        question['answer_b'],
        question['answer_c'],
        question['correct'],
        question['source']
    )
    try:
        cursor.execute(insert_query, insert_params)
    except sqlite3.DatabaseError as error:
        logger.error(f"There was an error during the question insert query: {error}")
        sys.exit()
    else:
        changed = cursor.execute("SELECT changes()").fetchone()[0]

        if changed == 0:  # nothing changed
            pass
        else:
            last_id = cursor.lastrowid
            if last_id is not None and last_id != 0:  # inserted new question
                logging.info(f"Inserted new question: {question['question']}")

                # add row for question's statistics
                insert_statistics_query = f"INSERT INTO {quiz_name}_statistics VALUES (?, ?, ?)"
                insert_statistics_params = (question['id'], 0, 0)
                try:
                    cursor.execute(insert_statistics_query, insert_statistics_params)
                except sqlite3.DatabaseError as error:
                    logger.error(f"There was an error during the question's statistics insert query: {error}")
                    sys.exit()
                except Exception as error:
                    logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")
                else:
                    logging.info(f"Question number {question['id']}'s statistics inserted successfully")
            else:  # existing question was updated
                logging.info(f"Question number {question['id']} updated")

                # clear statistics for updated question
                update_statistics_query = f"UPDATE {quiz_name}_statistics SET times_chosen=0, times_correct=0 WHERE question_id LIKE ?"
                update_statistics_params = (question['id'])
                try:
                    cursor.execute(update_statistics_query, update_statistics_params)
                except sqlite3.DatabaseError as error:
                    logger.error(f"There was an error during the question's statistics update query: {error}")
                    sys.exit()
                except Exception as error:
                    logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")
                else:
                    logging.info(f"Question numer {question['id']}'s statistics updated successfully")

def import_database(quiz_name: str, format_of_dataset:str):
    validate_inputs(quiz_name, format_of_dataset)

    quiz_name = quiz_name.replace("-", "_")

    try:
        with sqlite3.connect(os.getenv("DATABASE_PATH")) as database_connection:
            cursor = database_connection.cursor()

            create_tables(quiz_name, cursor)

            data_from_file = read_file(quiz_name, format_of_dataset)

            for question in data_from_file:
                insert_question(question, quiz_name, cursor)

            database_connection.commit()
    except sqlite3.DatabaseError as error:
        logger.error(f"There was an error with the database: {error}")
        sys.exit()
    except Exception as error:
        logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import new set of questions into database")
    parser.add_argument("path_to_dataset", type=str, help="Path to folder with dataset of questions")
    parser.add_argument("format_of_dataset", type=str, help="In which format is the dataset (CSV/JSON)",
                        choices=["csv", "json"])

    args = parser.parse_args()

    import_database(args.path_to_dataset, str(args.format_of_dataset).lower())

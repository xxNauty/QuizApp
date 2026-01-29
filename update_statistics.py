import os
import sqlite3
import logging

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

def update_statistics_for_question(quiz_name: str, id_of_question: int, correctly_answered: bool) -> None:
    try:
        with sqlite3.connect(os.getenv("DATABASE_PATH")) as database_connection:
            database_connection.row_factory = sqlite3.Row
            cursor = database_connection.cursor()

            select_query =f"SELECT * FROM {quiz_name}_statistics WHERE question_id LIKE {id_of_question}"
            try:
                cursor.execute(select_query)
            except sqlite3.DatabaseError as error:
                logger.error(f"There was an error during the fetch of the question's statistics: {error}")
            except Exception as error:
                logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")
            else:
                logger.info("Statistics read successfully")

            statistics = [dict(row) for row in cursor.fetchall()][0]
            statistics['times_chosen'] += 1
            if correctly_answered:
                statistics['times_correct'] += 1

            update_query = f"UPDATE {quiz_name}_statistics SET times_chosen=?, times_correct=? WHERE question_id LIKE ?"
            update_params = (statistics['times_chosen'], statistics['times_correct'], id_of_question)
            try:
                cursor.execute(update_query, update_params)
            except sqlite3.DatabaseError as error:
                logger.error(f"There was an error during the update of the question's statistics: {error}")
            except Exception as error:
                logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")
            else:
                logger.info("Statistics updated successfully")

            database_connection.commit()
    except sqlite3.DatabaseError as error:
        logger.error(f"There was an error during the connection with the database: {error}")
    except Exception as error:
        logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")
    else:
        logger.info("Statistics updated successfully")

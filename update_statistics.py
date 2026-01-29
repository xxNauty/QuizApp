import os
import sqlite3
import logging

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

def update_statistics_for_question(quiz_name: str, id_of_question: int, correctly_answered: bool) -> None:
    with sqlite3.connect(os.getenv("DATABASE_PATH")) as database_connection:
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()

        cursor.execute(f"SELECT * FROM {quiz_name}_statistics WHERE question_id LIKE {id_of_question}")

        statistics = [dict(row) for row in cursor.fetchall()][0]
        statistics['times_chosen'] += 1
        if correctly_answered:
            statistics['times_correct'] += 1

        update_query = f"""
            UPDATE {quiz_name}_statistics
            SET times_chosen=?, times_correct=?
            WHERE question_id LIKE ?
        """
        update_params = (statistics['times_chosen'], statistics['times_correct'], id_of_question)

        cursor.execute(update_query, update_params)

        database_connection.commit()

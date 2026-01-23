import logging
import sqlite3

from exception.NoDataFoundException import NoDataFoundError

logger = logging.getLogger('data_reader.py')

def read_database(quiz_name: str) -> list[dict]|None:
    try:
        database_connection = sqlite3.connect("database/database.db")
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()

        cursor.execute(f"SELECT * FROM {quiz_name}")

        data = [dict(row) for row in cursor.fetchall()]
        if len(data) == 0:
            raise NoDataFoundError()
        else:
            return data
    except NoDataFoundError:
        logger.error(f"There is no data inside the {quiz_name} table")
        return None
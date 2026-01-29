import logging
import sqlite3

from typing import List, Dict, Optional

from exception.NoDataFoundException import NoDataFoundError

logger = logging.getLogger(__name__)

def read_database(quiz_name: str) -> Optional[List[Dict]]:
    try:
        #validation of the inputs
        if not isinstance(quiz_name, str) or not quiz_name.isidentifier():
            raise ValueError("Invalid table name provided")

        #using with statement ensures the connection is automatically closed
        with sqlite3.connect("database/database.db") as database_connection:
            database_connection.row_factory = sqlite3.Row
            cursor = database_connection.cursor()

            cursor.execute(f"SELECT * FROM {quiz_name}")
            data = [dict(row) for row in cursor.fetchall()]

            if len(data) == 0:
                raise NoDataFoundError(quiz_name)
            else:
                return data
    except NoDataFoundError as error:
        logger.error(f"There was an error with the content of the database: {error}")
        return None
    except ValueError as error:
        logger.error(f"There was an error with the function parameter: {error}")
        return None
    except sqlite3.DatabaseError as error:
        logger.error(f"There was an error with the database: {error}")
        return None
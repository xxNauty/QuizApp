import os
import logging
import sqlite3

from dotenv import load_dotenv
from typing import List, Dict, Optional

from exception.NoDataFoundException import NoDataFoundError
from database.get_list_of_tables import get_list_of_tables

logger = logging.getLogger("main")
load_dotenv()

def read_database(quiz_name: str) -> Optional[List[Dict]]:
    try:
        #validation of the inputs
        if not isinstance(quiz_name, str) or quiz_name not in get_list_of_tables():
            raise ValueError("Invalid table name provided")

        with sqlite3.connect(os.getenv("DATABASE_PATH")) as database_connection:
            database_connection.row_factory = sqlite3.Row
            cursor = database_connection.cursor()

            cursor.execute(f"SELECT * FROM {quiz_name}")
            data = [dict(row) for row in cursor.fetchall()]

            if len(data) == 0:
                raise NoDataFoundError(quiz_name)
    except NoDataFoundError as error:
        logger.error(f"There was an error with the content of the database: {error}")
        return None
    except ValueError as error:
        logger.error(f"There was an error with the function parameter: {error}")
        return None
    except sqlite3.DatabaseError as error:
        logger.error(f"There was an error with the database: {error}")
        return None
    except Exception as error:
        logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")
        return None
    else:
        logger.info("Database read successfully")
        return data

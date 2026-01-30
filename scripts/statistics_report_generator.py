import os
import csv
import json
import sqlite3
import logging
import argparse

from datetime import datetime
from dotenv import load_dotenv

from database.get_list_of_tables import get_list_of_tables

logging.basicConfig(
    level=logging.INFO,
    filename=os.getenv("LOGS_PATH") + datetime.now().strftime("%Y_%m_%d") + ".log",
    filemode='a',
    format=os.getenv("LOGS_FORMAT"),
    encoding='utf-8'
)
logger = logging.getLogger("script")
load_dotenv()

def generate(quiz_name: str, format_of_report: str) -> None:
    try:
        if not isinstance(quiz_name, str) or quiz_name not in get_list_of_tables():
            raise ValueError("Invalid table name provided")
        if not isinstance(format_of_report, str) or format_of_report not in ['json', 'csv']:  # in future also PDF
            raise ValueError("Invalid or not supported format of report")
    except ValueError as error:
        logger.error(f"There was an error during the validation of inputs: {error}")
    except Exception as error:
        logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")
    else:
        logger.info("Given correct inputs")

    try:
        with sqlite3.connect(os.getenv("DATABASE_PATH")) as database_connection:
            database_connection.row_factory = sqlite3.Row
            cursor = database_connection.cursor()

            cursor.execute(f"""
                SELECT * FROM {quiz_name} 
                JOIN {quiz_name}_statistics 
                ON {quiz_name}.id = {quiz_name}_statistics.question_id
            """)
    except sqlite3.DatabaseError as error:
        logger.error(f"There was an error during the reading questions from the database: {error}")
    except Exception as error:
        logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")
    else:
        logger.info("Questions read with it's statistics")

    questions_with_statistics = [dict(row) for row in cursor.fetchall()]


    prepared_statistics = []
    additional_statistics = {
        "number_of_very_easy": 0,
        "number_of_easy": 0,
        "number_of_medium": 0,
        "number_of_hard": 0,
        "number_of_very_hard": 0,
    }

    for i in range(len(questions_with_statistics)):

        times_chosen = questions_with_statistics[i]['times_chosen']
        times_correct = questions_with_statistics[i]['times_correct']

        if times_chosen == 0:
            percent_correct = None
            difficulty_level = "unknown"
        else:
            percent_correct = round(times_correct/times_chosen*100, 2)
            if 80 < percent_correct <= 100:
                difficulty_level = "very easy"
                additional_statistics['number_of_very_easy'] += 1
            elif 60 < percent_correct <= 80:
                difficulty_level = "easy"
                additional_statistics['number_of_easy'] += 1
            elif 40 < percent_correct <= 60:
                difficulty_level = "medium"
                additional_statistics['number_of_medium'] += 1
            elif 20 < percent_correct <= 40:
                difficulty_level = "hard"
                additional_statistics['number_of_hard'] += 1
            else:
                difficulty_level = "very hard"
                additional_statistics['number_of_very_hard'] += 1

        statistics_for_question = {
            'question': questions_with_statistics[i]['question'],
            'times_chosen': times_chosen,
            'times_correct': times_correct,
            'percent_correct': percent_correct,
            'difficulty': difficulty_level
        }

        prepared_statistics.append(statistics_for_question)

    os.makedirs("reports", exist_ok=True)

    try:
        match format_of_report.lower():
            case "csv":
                _generate_csv(prepared_statistics)
            case "json":
                _generate_json(prepared_statistics)
            case "pdf":
                _generate_pdf(prepared_statistics, additional_statistics)
    except NotImplementedError as error:
        logger.error(f"There was an error during the generation of the report: {error}")
    except Exception as error:
        logger.error(f"AN UNEXPECTED ERROR HAPPENED: {error}")
    else:
        logger.info("Report generated successfully")


def _generate_csv(statistics: list[dict]) -> None:
    field_names = ['question', 'times_chosen', 'times_correct', 'percent_correct', 'difficulty']

    try:
        with open(os.getenv("REPORTS_PATH") + datetime.now().strftime(os.getenv("REPORTS_DATA_FORMAT")) + ".csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names) # statistics[0].keys()
            writer.writeheader()
            writer.writerows(statistics)
    except IOError as error:
        logger.error(f"There was an error during the writing to a CSV file: {error}")
    except csv.Error as error:
        logger.error(f"There was an error related with a CSV module: {error}")
    else:
        logger.info("CSV report created")

def _generate_json(statistics: list[dict]) -> None:
    try:
        with open(os.getenv("REPORTS_PATH") + datetime.now().strftime(os.getenv("REPORTS_DATA_FORMAT")) + ".json", "w", encoding="utf-8") as file:
            json.dump(statistics, file, indent=2, ensure_ascii=False) # ensure_ascii=False to keep polish characters as they are
    except IOError as error:
        logger.error(f"There was an error during the writing to a JSON file: {error}")
    except json.JSONDecodeError as error:
        logger.error(f"There was an error related with a JSON module: {error}")
    else:
        logger.info("JSON report created")

def _generate_pdf(statistics: list[dict], additional_statistics: dict) -> None:
    raise NotImplementedError("PDF report generation not implemented yet")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate report with statistics of every question")
    parser.add_argument("quiz_name", type=str, help="Name of quiz you want to generate statistics of.")
    parser.add_argument("format_of_report", type=str, help="Choose format in which you want this report. (json/csv/pdf)", choices=['json', 'csv', 'pdf'])

    args = parser.parse_args()

    generate(args.quiz_name, args.format_of_report)
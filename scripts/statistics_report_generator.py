import csv
import json
import sqlite3
import logging
import argparse

from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    filename=f"scripts/script_logs/statistics_report_generator/{datetime.now().strftime("%Y_%m_%d")}_logs.log",
    filemode='a',
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger("statistics_report_generator.py")

def generate(quiz_name: str, format_of_report: str) -> None:
    database_connection = sqlite3.connect("database/database.db")
    database_connection.row_factory = sqlite3.Row
    cursor = database_connection.cursor()

    cursor.execute(f"""
        SELECT * FROM {quiz_name} 
        JOIN {quiz_name}_statistics 
        ON {quiz_name}.id = {quiz_name}_statistics.question_id
    """)

    questions_with_statistics = [dict(row) for row in cursor.fetchall()]
    logger.info("Questions read with it's statistisc")

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

    match format_of_report.lower():
        case "csv":
            _generate_csv(prepared_statistics)
        case "json":
            _generate_json(prepared_statistics)
        case "pdf":
            _generate_pdf(prepared_statistics, additional_statistics)


def _generate_csv(statistics: list[dict]) -> None:
    field_names = ['question', 'times_chosen', 'times_correct', 'percent_correct', 'difficulty']

    with open(f"reports/statistics_{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(statistics)

        file.close()

def _generate_json(statistics: list[dict]) -> None:
    with open(f"reports/statistics_{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}.json", "w", encoding="utf-8") as file:
        json.dump(statistics, file, indent=2, ensure_ascii=False) # ensure_ascii=False to keep polish characters as they are
        file.close()

def _generate_pdf(statistics: list[dict], additional_statistics: dict) -> None:
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate report with statistics of every question")
    parser.add_argument("quiz_name", type=str, help="Name of quiz you want to generate statistics of.")
    parser.add_argument("format_of_report", type=str, help="Choose format in which you want this report. (JSON/CSV/PDF)")

    args = parser.parse_args()

    generate(args.quiz_name, args.format_of_report)
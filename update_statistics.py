import sqlite3

def update_statistics_for_question(name_of_quiz: str, id_of_question: int, correctly_answered: bool) -> None:
    database_connection = sqlite3.connect(f"database/database.db")
    database_connection.row_factory = sqlite3.Row
    cursor = database_connection.cursor()

    cursor.execute(f"SELECT * FROM {name_of_quiz}_statistics WHERE question_id LIKE {id_of_question}")

    current_statistics = [dict(row) for row in cursor.fetchall()][0]
    current_statistics['times_chosen'] += 1
    if correctly_answered:
        current_statistics['times_correct'] += 1

    cursor.execute(f"""
        UPDATE {name_of_quiz}_statistics 
        SET 
        times_chosen = {current_statistics['times_chosen']}, times_correct = {current_statistics['times_correct']}
        WHERE question_id LIKE {id_of_question}
        """)

    database_connection.commit()
    database_connection.close()

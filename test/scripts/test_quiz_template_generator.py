import os

import pytest
import shutil
import logging

from pathlib import Path
from datetime import datetime
from scripts import quiz_template_generator

@pytest.fixture(autouse=True)
def clear_database_after_tests():
    yield
    for item in os.listdir("database"):
        item_path = os.path.join("database", item)

        if os.path.isdir(item_path) and item.startswith("__test"):
            shutil.rmtree(item_path)

params_for_test_for_correct_data = [
    pytest.param('__test_quiz_1', "csv", 20, 18, id="Fully correct"),
    pytest.param('__test quiz 2', 'json', 30, 10, id="Quiz name contains spaces"),
    pytest.param('__test-quiz-3', 'CSV', 10, 1, id="Database format written in uppercase")
]
@pytest.mark.parametrize("name_of_quiz, db_format, num_of_questions, min_to_pass", params_for_test_for_correct_data)
def test_for_correct_data(caplog, monkeypatch, name_of_quiz, db_format, num_of_questions, min_to_pass):
    data_path = Path("database")
    data_files_before = [f.name for f in data_path.iterdir() if f.is_dir()]

    assert name_of_quiz not in data_files_before

    inputs_iterator = iter([name_of_quiz, db_format, num_of_questions, min_to_pass])

    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs_iterator))
    name_of_quiz = name_of_quiz.replace(" ", "-")

    with caplog.at_level(logging.INFO):
        quiz_template_generator.generate()

    assert f"Directory for quiz created successfully. Quiz data stored inside: database/{name_of_quiz}/" in caplog.messages
    assert "Configuration file created" in caplog.messages
    assert "Configuration file filled with data" in caplog.messages
    assert "Database for questions created" in caplog.messages

    data_files_after = [f.name for f in data_path.iterdir() if f.is_dir()]
    assert len(data_files_after) - len(data_files_before) == 1

    assert name_of_quiz in data_files_after

    quiz_data_path = Path(f"database/{name_of_quiz}")
    quiz_data_files = [f.name for f in quiz_data_path.iterdir() if f.is_file()]

    assert "data.json" or "data.csv" in quiz_data_files
    assert "config.yaml" in quiz_data_files

    with open(f"database/{name_of_quiz}/config.yaml", 'r') as file:
        config_data = file.read().split("\n")
        assert "quiz_name" in config_data[0]
        assert "number_of_questions" in config_data[1]
        assert "minimum_to_pass" in config_data[2]

params_for_test_for_wrong_database_format = [
    pytest.param("__test-quiz-4", ["html", "css", "123", "qwe", "csv"], 20, 12, id="Four times incorrect, then CSV"),
    pytest.param("__test-quiz-5", ["css", "json"], 30, 12, id="Once incorrect, then JSON"),
    pytest.param("__test-quiz-6", ["jsonnnnnnnn", "json"], 30, 12, id="Once incorrect JSON, then correct JSON")
]
@pytest.mark.parametrize("name_of_quiz, db_format, num_of_questions, min_to_pass", params_for_test_for_wrong_database_format)
def test_for_wrong_database_format(caplog, capsys, monkeypatch, name_of_quiz, db_format, num_of_questions, min_to_pass):
    data_path = Path("database")
    data_files_before = [f.name for f in data_path.iterdir() if f.is_dir()]

    assert name_of_quiz not in data_files_before

    inputs_iterator = iter([name_of_quiz, *db_format, num_of_questions, min_to_pass])
    print(db_format)

    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs_iterator))
    name_of_quiz = name_of_quiz.replace(" ", "-")

    with caplog.at_level(logging.INFO):
        quiz_template_generator.generate()
    print_output = capsys.readouterr().out.splitlines()

    assert len(db_format) - 1 == print_output.count("Only JSON and CSV are accepted")
    assert len(db_format) - 1 == caplog.messages.count("Chosen incorrect database format")
    assert f"Directory for quiz created successfully. Quiz data stored inside: database/{name_of_quiz}/" in caplog.messages
    assert "Configuration file created" in caplog.messages
    assert "Configuration file filled with data" in caplog.messages
    assert "Database for questions created" in caplog.messages

    data_files_after = [f.name for f in data_path.iterdir() if f.is_dir()]
    assert len(data_files_after) - len(data_files_before) == 1

    assert name_of_quiz in data_files_after

    quiz_data_path = Path(f"database/{name_of_quiz}")
    quiz_data_files = [f.name for f in quiz_data_path.iterdir() if f.is_file()]

    assert "data.json" or "data.csv" in quiz_data_files
    assert "config.yaml" in quiz_data_files

    with open(f"database/{name_of_quiz}/config.yaml", 'r') as file:
        config_data = file.read().split("\n")
        assert "quiz_name" in config_data[0]
        assert "number_of_questions" in config_data[1]
        assert "minimum_to_pass" in config_data[2]

params_for_test_for_min_to_pass_higher_than_num_of_questions = [
    pytest.param("__test-quiz-7", "csv", 20, [21, 19], id="First too high, then correct")
]
@pytest.mark.parametrize("name_of_quiz, db_format, num_of_questions, min_to_pass", params_for_test_for_min_to_pass_higher_than_num_of_questions)
def test_for_min_to_pass_higher_than_num_of_questions(caplog, capsys, monkeypatch, name_of_quiz, db_format, num_of_questions, min_to_pass):
    data_path = Path("database")
    data_files_before = [f.name for f in data_path.iterdir() if f.is_dir()]

    assert name_of_quiz not in data_files_before

    inputs_iterator = iter([name_of_quiz, db_format, num_of_questions, *min_to_pass])

    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs_iterator))
    name_of_quiz = name_of_quiz.replace(" ", "-")

    with caplog.at_level(logging.INFO):
        quiz_template_generator.generate()
    print_output = capsys.readouterr().out.splitlines()

    assert len(min_to_pass) - 1 == print_output.count("This number cannot be greater than total number of questions in quiz")
    assert len(min_to_pass) - 1 == caplog.messages.count("Chosen higher min_to_pass than total number of questions")
    assert f"Directory for quiz created successfully. Quiz data stored inside: database/{name_of_quiz}/" in caplog.messages
    assert "Configuration file created" in caplog.messages
    assert "Configuration file filled with data" in caplog.messages
    assert "Database for questions created" in caplog.messages

    data_files_after = [f.name for f in data_path.iterdir() if f.is_dir()]
    assert len(data_files_after) - len(data_files_before) == 1

    assert name_of_quiz in data_files_after

    quiz_data_path = Path(f"database/{name_of_quiz}")
    quiz_data_files = [f.name for f in quiz_data_path.iterdir() if f.is_file()]

    assert "data.json" or "data.csv" in quiz_data_files
    assert "config.yaml" in quiz_data_files

    with open(f"database/{name_of_quiz}/config.yaml", 'r') as file:
        config_data = file.read().split("\n")
        assert "quiz_name" in config_data[0]
        assert "number_of_questions" in config_data[1]
        assert "minimum_to_pass" in config_data[2]

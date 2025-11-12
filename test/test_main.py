# GENERATED WITH GITHUB COPILOT

import os
import json
import types
import builtins
import logging
import pytest
import main

# sprawdza czy podana ścieżka istnieje, jeśli nie to ją tworzy
def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

# tworzy plik konfiguracyjny używany na czas testów
def _write_config(directory: str, number_of_questions: int, minimum_to_pass: int) -> None:
    _ensure_dir(directory)
    with open(os.path.join(directory, "config.yaml"), "w", encoding="utf-8") as f:
        f.write(f"number_of_questions: {number_of_questions}\n")
        f.write(f"minimum_to_pass: {minimum_to_pass}\n")

# tworzy pusty plik
def _write_empty_file(directory: str, name: str) -> None:
    _ensure_dir(directory)
    with open(os.path.join(directory, name), "w", encoding="utf-8") as f:
        f.write("")

# zapisuje dane w formacie JSON do pliku
def _write_data_json(directory: str, data) -> None:
    _ensure_dir(directory)
    with open(os.path.join(directory, "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

# usuwa pliki utworzone na czas testów
def _cleanup_files(directory: str):
    for file_name in ("config.yaml", "data.json", "data.csv"):
        try:
            os.remove(os.path.join(directory, file_name))
        except FileNotFoundError:
            pass

def _sample_questions():
    return [
        {
            "PYTANIE": "Ile to jest 1 + 1",
            "ODP_A": "2",
            "ODP_B": "3",
            "ODP_C": "4",
            "POPRAWNA": "A",
            "NUMER_PYTANIA": 1,
        },
        {
            "PYTANIE": "Stolica Polski",
            "ODP_A": "Berlin",
            "ODP_B": "Warszawa",
            "ODP_C": "Paryż",
            "POPRAWNA": "B",
            "NUMER_PYTANIA": 2,
        },
        {
            "PYTANIE": "Ile okręgów jest w logo AUDI",
            "ODP_A": "2",
            "ODP_B": "6",
            "ODP_C": "4",
            "POPRAWNA": "C",
            "NUMER_PYTANIA": 3,
        },
    ]

def test_read_configuration_from_file(tmp_path):
    directory = tmp_path / "data"
    dir_str = str(directory) + os.sep
    _write_config(dir_str, number_of_questions=4, minimum_to_pass=3)

    number, minimum = main.read_configuration_of_quiz(dir_str)

    assert number == 4
    assert minimum == 3

    _cleanup_files(dir_str)

def test_read_configuration_prompts_when_missing(monkeypatch, caplog, tmp_path):
    directory = tmp_path / "data_missing"
    dir_str = str(directory) + os.sep
    try:
        os.remove(os.path.join(dir_str, "config.yaml"))
    except Exception:
        pass

    inputs = iter(["7", "5"])

    def fake_input(prompt=""):
        return next(inputs)

    monkeypatch.setattr(builtins, "input", fake_input)

    with caplog.at_level(logging.ERROR):
        number, minimum = main.read_configuration_of_quiz(dir_str)

    assert number == 7
    assert minimum == 5
    assert any("There is no file with configuration" in m for m in caplog.messages)

def test_read_question_database_prefers_json(tmp_path, monkeypatch):
    directory = tmp_path / "data_json"
    dir_str = str(directory) + os.sep
    _write_empty_file(dir_str, "data.json")

    sentinel = [{"some": "question"}]

    monkeypatch.setattr(main, "json_reader", types.SimpleNamespace(read_file=lambda _: sentinel))
    monkeypatch.setattr(main, "csv_reader", types.SimpleNamespace(read_file=lambda _: []))

    result = main.read_question_database(dir_str)
    assert result is sentinel

    _cleanup_files(dir_str)

def test_read_question_database_falls_back_to_csv(tmp_path, monkeypatch):
    directory = tmp_path / "data_csv"
    dir_str = str(directory) + os.sep
    _write_empty_file(dir_str, "data.csv")

    sentinel = [{"csv": "question"}]
    monkeypatch.setattr(main, "csv_reader", types.SimpleNamespace(read_file=lambda _: sentinel))
    monkeypatch.setattr(main, "json_reader", types.SimpleNamespace(read_file=lambda _: []))

    result = main.read_question_database(dir_str)
    assert result is sentinel

    _cleanup_files(dir_str)

def test_read_question_database_no_files_logs_error(tmp_path, caplog, monkeypatch):
    directory = tmp_path / "data_none"
    dir_str = str(directory) + os.sep

    with caplog.at_level(logging.ERROR):
        result = main.read_question_database(dir_str)

    assert result is None
    assert any("There is no file with questions" in m for m in caplog.messages)

@pytest.mark.parametrize(
    "choices, expected_substring",
    [
        (["a", "b", "c"], "Congratulations"),
        (["a", "a", "a"], "You failed"),
    ],
)
def test_play_behaviour(tmp_path, monkeypatch, capsys, choices, expected_substring):
    directory = tmp_path / "play_data"
    dir_str = str(directory) + os.sep

    questions = _sample_questions()

    _write_config(dir_str, number_of_questions=2, minimum_to_pass=2)
    _write_empty_file(dir_str, "data.json")

    monkeypatch.setattr(main, "json_reader", types.SimpleNamespace(read_file=lambda _: questions))
    monkeypatch.setattr(main, "csv_reader", types.SimpleNamespace(read_file=lambda _: []))

    def fake_generate_quiz(qs, n):
        return qs[:n]

    monkeypatch.setattr(main, "quiz_generator", types.SimpleNamespace(generate_quiz=fake_generate_quiz))

    choice_iter = iter(choices)

    def fake_input(prompt=""):
        try:
            return next(choice_iter)
        except StopIteration:
            raise RuntimeError("No more input values provided in test")

    monkeypatch.setattr(builtins, "input", fake_input)

    main.play(dir_str)

    captured = capsys.readouterr()
    out = captured.out

    assert "The quiz starts" in out
    assert expected_substring in out

    _cleanup_files(dir_str)

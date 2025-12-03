import shutil
import tempfile
from typing import Any, Generator

import pytest
import os

from pathlib import Path
from scripts import quiz_template_generator

# tworzenie wirtualnego środowiska do uruchamiania testów
@pytest.fixture()
def isolated_cwd() -> Generator[Path, Any, None]:
    old_cwd = os.getcwd()
    tmp_dir = tempfile.mkdtemp(prefix="pytest-isolated-env-")
    os.chdir(tmp_dir)
    try:
        yield Path(tmp_dir)
    finally:
        os.chdir(old_cwd)
        shutil.rmtree(tmp_dir, ignore_errors=True)

@pytest.mark.parametrize(
    "name, file_format, number_of_questions, minimum_to_pass",
    [
        ("First_quiz", "csv", 20, 12),
        ("second-quiz", "json", 100, 100)
    ]
)
@pytest.mark.skip()
def test_for_correct_data(isolated_cwd, monkeypatch, name: str, file_format: str, number_of_questions: int, minimum_to_pass: int) -> None:
    inputs = iter([name, file_format, number_of_questions, minimum_to_pass])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs)) # symulowanie danych wprowadzonych przez użytkownika

    quiz_template_generator.generate("./")

    assert os.path.exists(f"./{name}")

    assert os.path.exists(f"./{name}/data.{file_format}")
    assert os.path.exists(f"./{name}/config.yaml")

    with open(f"./{name}/config.yaml", 'r') as file:
        content = file.read().split("\n")
        assert content[0] == "number_of_questions: " + str(number_of_questions)
        assert content[1] == "minimum_to_pass: " + str(minimum_to_pass)

@pytest.mark.parametrize(
    "name, file_format, number_of_questions, minimum_to_pass",
    [
        ("First_quiz", ["HTML", "CSS", "", "dog", "Json"], 20, 12),
    ]
)
@pytest.mark.skip()
def test_for_incorrect_file_formats(isolated_cwd, monkeypatch, name: str, file_format: str, number_of_questions: int, minimum_to_pass: int) -> None:
    inputs = iter([name, *file_format, number_of_questions, minimum_to_pass]) # * przy file_format oznacza rozpakowywanie listy
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    quiz_template_generator.generate("./")

    assert os.path.exists(f"./{name}")

    assert os.path.exists(f"./{name}/data.json")
    assert os.path.exists(f"./{name}/config.yaml")

    with open(f"./{name}/config.yaml", 'r') as file:
        content = file.read().split("\n")
        assert content[0] == "number_of_questions: " + str(number_of_questions)
        assert content[1] == "minimum_to_pass: " + str(minimum_to_pass)

@pytest.mark.parametrize(
    "name, file_format, number_of_questions, minimum_to_pass",
    [
        ("First_quiz", "csv", 20, [22, 99, 12]),
    ]
)
@pytest.mark.skip()
def test_for_min_to_pass_greater_than_num_of_questions(isolated_cwd, monkeypatch, name: str, file_format: str, number_of_questions: int, minimum_to_pass: int) -> None:
    inputs = iter([name, file_format, number_of_questions, *minimum_to_pass])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    quiz_template_generator.generate("./")

    assert os.path.exists(f"./{name}")

    assert os.path.exists(f"./{name}/data.{file_format}")
    assert os.path.exists(f"./{name}/config.yaml")

    with open(f"./{name}/config.yaml", 'r') as file:
        content = file.read().split("\n")
        assert content[0] == "number_of_questions: " + str(number_of_questions)
        assert content[1] == "minimum_to_pass: " + str(12)
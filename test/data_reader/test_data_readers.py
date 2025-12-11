import logging

import pytest

from data import data_reader

@pytest.mark.parametrize(
    "file_format",
    [
        "csv",
        "json"
    ]
)
def test_for_correct_file(caplog, file_format):
    data = []

    with caplog.at_level(logging.INFO):
        match file_format:
            case "json":
                data = data_reader.read_file("test/data_reader/data/data.json", 'json')
            case "csv":
                data = data_reader.read_file("test/data_reader/data/data.csv", 'csv')

    assert type(data) == list
    assert len(data) == 10

    assert f"Questions read successfully from the data.{file_format} file({file_format.upper()}), there are 10 questions" in caplog.messages

    for element in data:
        assert len(element) is 7

        assert "id" in element
        assert type(element['id']) is int

        assert "question" in element
        assert type(element['question']) is str

        assert 'answer_a' in element
        assert type(element['answer_a']) is str

        assert 'answer_b' in element
        assert type(element['answer_b']) is str

        assert 'answer_c' in element
        assert type(element['answer_c']) is str

        assert 'correct' in element
        assert type(element['correct']) is str
        assert len(element['correct']) == 1
        assert element['correct'] in ['a', 'b', 'c']

        assert 'source' in element
        assert type(element['source']) is str

@pytest.mark.parametrize(
    "file_format",
    [
        "csv",
        "json"
    ]
)
def test_for_non_existing_file(caplog, file_format):
    data = []

    with caplog.at_level(logging.ERROR):
        match file_format:
            case "json":
                data = data_reader.read_file("test/data_reader/data/not_exist.json", 'json')
            case "csv":
                data = data_reader.read_file("test/data_reader/data/not_exist.csv", 'csv')

    assert data is None
    assert f"There is no such file as not_exist.{file_format}" in caplog.messages
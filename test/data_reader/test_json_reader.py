import os
import logging

from data_reader import json_reader
from test.data_reader import data_for_test_json_reader

EXISTING_FILE = "data.json"

def test_for_existing_file(caplog):
    _prepare_file_for_test()

    with caplog.at_level(logging.INFO):
        content = json_reader.read_file(EXISTING_FILE, encoding='cp1252')

    assert "Questions read successfully from the data.json file(JSON), there are 10 questions" in caplog.messages

    assert type(content) == list
    assert len(content) == 10

    assert len(content[0]) == 6

    _cleanup_after_tests()

def test_for_non_existing_file(caplog):
    with caplog.at_level(logging.ERROR):
        content = json_reader.read_file("non_existing_file.json")

    assert "There is no such file as non_existing_file.json" in caplog.messages

    assert content is None

def _prepare_file_for_test() -> None:
    with open(EXISTING_FILE, 'w') as file:
        file.write(data_for_test_json_reader.CONTENT_OF_EXISTING_FILE)
        file.close()

def _cleanup_after_tests() -> None:
    os.remove(EXISTING_FILE)
import os
import logging
import pytest

from data_reader import csv_reader

from test.data_reader import data_for_test_csv_reader

EXISTING_FILE = "test/data_reader/data.csv"

@pytest.mark.skip()
def test_for_existing_file(caplog) -> None:
    _prepare_file_for_test()
    with caplog.at_level(logging.INFO):
        content = csv_reader.read_file(EXISTING_FILE, encoding='cp1252')

    assert "Questions read successfully from the data.csv file(CSV), there are 10 questions" in caplog.messages

    assert type(content) == list
    assert len(content) == 10

    assert len(content[0]) == 6

    _cleanup_after_tests()

@pytest.mark.skip()
def test_for_non_existing_file(caplog) -> None:
    with caplog.at_level(logging.ERROR):
        content = csv_reader.read_file("non_existing_file.csv")

    assert "There is no such file as non_existing_file.csv" in caplog.messages

    assert content is None

def _prepare_file_for_test() -> None:
    with open(EXISTING_FILE, 'w') as file:
        file.write(data_for_test_csv_reader.CONTENT_OF_EXISTING_FILE)
        file.close()

def _cleanup_after_tests() -> None:
    os.remove(EXISTING_FILE)
import logging
import os

from data_reader import csv_reader

EXISTING_FILE = "test/data_reader/data.csv"
CONTENT_OF_EXISTING_FILE = """id,name,email,phone,company,created_at
1,Alice Johnson,alice.johnson@example.com,555-0101,Acme Corp,2025-01-15T09:12:34Z
2,Bob Smith,bob.smith@example.net,555-0102,Smith LLC,2025-02-20T14:05:10Z
3,Carlos Rivera,c.rivera@example.org,555-0103,Rivera & Co,2025-03-05T08:22:45Z
4,Diana Chen,diana.chen@example.com,555-0104,NextGen Inc,2025-03-18T11:47:00Z
5,Ethan Patel,ethan.patel@example.com,555-0105,Patel Industries,2025-04-02T16:30:12Z
6,Fatima Al-Masri,fatima.alm@example.com,555-0106,Global Solutions,2025-04-10T07:20:55Z
7,George O'Neill,george.oneill@example.co.uk,555-0107,O'Neill Consulting,2025-05-01T12:00:00Z
8,Hannah Mueller,hannah.mueller@example.de,555-0108,Müller GmbH,2025-05-15T09:45:33Z
9,Ian Wright,ian.wright@example.com,555-0109,Wright Enterprises,2025-06-01T18:10:05Z
10,Jessie Lee,jessie.lee@example.com,555-0110,Lee & Partners,2025-06-20T13:55:21Z"""

def test_for_existing_file(caplog) -> None:
    _prepare_file_for_test()
    with caplog.at_level(logging.INFO):
        content = csv_reader.read_file(EXISTING_FILE, encoding='cp1252')

    assert "Questions read successfully from the data.csv file, there are 10 questions" in caplog.messages

    assert type(content) == list
    assert len(content) == 10

    assert len(content[0]) == 6

    _cleanup_after_tests()

def test_for_non_existing_file(caplog) -> None:
    with caplog.at_level(logging.ERROR):
        content = csv_reader.read_file("non_existing_file.csv")

    assert "There is no such file as non_existing_file.csv" in caplog.messages

    assert content is None

def _prepare_file_for_test() -> None:
    with open(EXISTING_FILE, 'w') as file:
        file.write(CONTENT_OF_EXISTING_FILE)
        file.close()

def _cleanup_after_tests() -> None:
    os.remove(EXISTING_FILE)
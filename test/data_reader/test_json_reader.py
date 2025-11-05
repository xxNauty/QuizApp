import os
import logging

from data_reader import json_reader

EXISTING_FILE = "data.json"

CONTENT_OF_EXISTING_FILE = """
[
  {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice.johnson@example.com",
    "phone": "555-0101",
    "company": "Acme Corp",
    "created_at": "2025-01-15T09:12:34Z"
  },
  {
    "id": 2,
    "name": "Bob Smith",
    "email": "bob.smith@example.net",
    "phone": "555-0102",
    "company": "Smith LLC",
    "created_at": "2025-02-20T14:05:10Z"
  },
  {
    "id": 3,
    "name": "Carlos Rivera",
    "email": "c.rivera@example.org",
    "phone": "555-0103",
    "company": "Rivera & Co",
    "created_at": "2025-03-05T08:22:45Z"
  },
  {
    "id": 4,
    "name": "Diana Chen",
    "email": "diana.chen@example.com",
    "phone": "555-0104",
    "company": "NextGen Inc",
    "created_at": "2025-03-18T11:47:00Z"
  },
  {
    "id": 5,
    "name": "Ethan Patel",
    "email": "ethan.patel@example.com",
    "phone": "555-0105",
    "company": "Patel Industries",
    "created_at": "2025-04-02T16:30:12Z"
  },
  {
    "id": 6,
    "name": "Fatima Al-Masri",
    "email": "fatima.alm@example.com",
    "phone": "555-0106",
    "company": "Global Solutions",
    "created_at": "2025-04-10T07:20:55Z"
  },
  {
    "id": 7,
    "name": "George O'Neill",
    "email": "george.oneill@example.co.uk",
    "phone": "555-0107",
    "company": "O'Neill Consulting",
    "created_at": "2025-05-01T12:00:00Z"
  },
  {
    "id": 8,
    "name": "Hannah Mueller",
    "email": "hannah.mueller@example.de",
    "phone": "555-0108",
    "company": "Müller GmbH",
    "created_at": "2025-05-15T09:45:33Z"
  },
  {
    "id": 9,
    "name": "Ian Wright",
    "email": "ian.wright@example.com",
    "phone": "555-0109",
    "company": "Wright Enterprises",
    "created_at": "2025-06-01T18:10:05Z"
  },
  {
    "id": 10,
    "name": "Jessie Lee",
    "email": "jessie.lee@example.com",
    "phone": "555-0110",
    "company": "Lee & Partners",
    "created_at": "2025-06-20T13:55:21Z"
  }
]"""

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
        file.write(CONTENT_OF_EXISTING_FILE)
        file.close()

def _cleanup_after_tests() -> None:
    os.remove(EXISTING_FILE)
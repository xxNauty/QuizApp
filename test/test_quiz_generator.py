import logging
import pytest

import quiz_generator

from test import data_for_test_quiz_generator # wymaga __init__.py do działania

def test_for_correct_data(caplog) -> None:
    with caplog.at_level(logging.INFO):
        quiz = quiz_generator.generate_quiz(data_for_test_quiz_generator.TEST_DATA, 5)

    list_of_ids = set()
    for question in quiz:
        id_of_question = question['NUMER_PYTANIA']
        list_of_ids.add(id_of_question)
        assert f"Chosen question number {id_of_question}" in caplog.messages

    assert len(list_of_ids) == 5

    assert type(quiz) is list
    assert type(quiz[0]) is dict

    assert len(quiz) == 5

    assert "Quiz generated, there are 5 questions" in caplog.messages

def test_for_incorrect_input_data(caplog) -> None:
    with pytest.raises(TypeError) as error:
        quiz_generator.generate_quiz("incorrect datatype", 5)

    assert str(error.value) == "Quiz can be generated only from list of questions, not <class 'str'>"
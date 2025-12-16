import pytest
import logging

from database import quiz_generator

SAMPLE_DATABASE_OF_QUESTIONS = [
    {"id": 1, "question": "question1", "answer_a": "ans_a", "answer_b": "ans_b", "answer_c": "ans_", "correct": "a", "source": "---"},
    {"id": 2, "question": "question2", "answer_a": "ans_aa", "answer_b": "ans_", "answer_c": "ansc", "correct": "b", "source": "---"},
    {"id": 3, "question": "question3", "answer_a": "ans_", "answer_b": "ans", "answer_c": "ans_c", "correct": "c", "source": "---"},
    {"id": 4, "question": "question4", "answer_a": "ans_aaaa", "answer_b": "ans_bbbb", "answer_c": "ans_ccc", "correct": "a", "source": "---"},
    {"id": 5, "question": "question5", "answer_a": "ans_aaa", "answer_b": "ans_bbb", "answer_c": "ans_c", "correct": "c", "source": "---"},
]
@pytest.mark.parametrize(
    "num_of_questions",
    [
        3,
        5
    ]
)
def test_for_correct_input(caplog, num_of_questions):
    with caplog.at_level(logging.INFO):
        drawn_questions = quiz_generator.generate_quiz(SAMPLE_DATABASE_OF_QUESTIONS, num_of_questions)

    assert type(drawn_questions) == list
    assert len(drawn_questions) == num_of_questions

    for question in drawn_questions:
        assert type(question) == dict

        assert "id" in question
        assert type(question['id']) == int

        assert "question" in question
        assert type(question['question']) == str

        assert "answer_a" in question
        assert type(question['answer_a']) == str

        assert "answer_b" in question
        assert type(question['answer_b']) == str

        assert "answer_c" in question
        assert type(question['answer_c']) == str

        assert "correct" in question
        assert type(question['correct']) == str
        assert len(question['correct']) == 1
        assert question['correct'] in ['a', 'b', 'c']

        assert "source" in question
        assert type(question['source']) == str

@pytest.mark.parametrize(
    "num_of_questions",
    [
        8
    ]
)
def test_for_not_enough_questions_in_database(caplog, num_of_questions):
    with caplog.at_level(logging.ERROR):
        drawn_questions = quiz_generator.generate_quiz(SAMPLE_DATABASE_OF_QUESTIONS, num_of_questions)

    assert "There is not enough questions in database to form such long quiz" in caplog.messages
    assert drawn_questions is None


from random import Random

import pytest

from memory_trainer.quiz import (
    MAX_FACTOR,
    MIN_FACTOR,
    MultiplicationQuestion,
    MultiplicationQuiz,
)


def test_question_answer_property() -> None:
    question = MultiplicationQuestion(3, 7)
    assert question.answer == 21


def test_generate_respects_range() -> None:
    quiz = MultiplicationQuiz.generate(num_questions=10, rng=Random(123))

    assert len(quiz.questions) == 10
    for question in quiz.questions:
        assert MIN_FACTOR <= question.left <= MAX_FACTOR
        assert MIN_FACTOR <= question.right <= MAX_FACTOR


def test_grade_counts_correct_answers() -> None:
    quiz = MultiplicationQuiz(
        [MultiplicationQuestion(2, 3), MultiplicationQuestion(4, 5)]
    )

    correct, total = quiz.grade([6, 21])

    assert total == 2
    assert correct == 1


def test_grade_treats_non_numeric_as_incorrect() -> None:
    quiz = MultiplicationQuiz([MultiplicationQuestion(2, 3)])

    correct, total = quiz.grade([None])

    assert total == 1
    assert correct == 0


def test_generate_requires_positive_number_of_questions() -> None:
    with pytest.raises(ValueError):
        MultiplicationQuiz.generate(num_questions=0)

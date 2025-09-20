"""Utilities for creating and grading multiplication quizzes."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import List, Optional, Sequence, Tuple

MIN_FACTOR = 2
MAX_FACTOR = 12


@dataclass(frozen=True)
class MultiplicationQuestion:
    """A single multiplication question."""

    left: int
    right: int

    @property
    def answer(self) -> int:
        """Return the expected answer for the question."""

        return self.left * self.right


@dataclass
class MultiplicationQuiz:
    """A collection of multiplication questions with grading helpers."""

    questions: List[MultiplicationQuestion]

    @classmethod
    def generate(
        cls, num_questions: int = 10, rng: Optional[Random] = None
    ) -> "MultiplicationQuiz":
        """Return a quiz populated with random multiplication questions."""

        if num_questions <= 0:
            raise ValueError("num_questions must be a positive integer")

        randomizer = rng or Random()
        questions = [
            MultiplicationQuestion(
                randomizer.randint(MIN_FACTOR, MAX_FACTOR),
                randomizer.randint(MIN_FACTOR, MAX_FACTOR),
            )
            for _ in range(num_questions)
        ]
        return cls(questions)

    def grade(self, responses: Sequence[Optional[int]]) -> Tuple[int, int]:
        """Return the number of correct answers and total number of questions."""

        correct = 0
        for index, question in enumerate(self.questions):
            response = responses[index] if index < len(responses) else None
            if response == question.answer:
                correct += 1
        return correct, len(self.questions)

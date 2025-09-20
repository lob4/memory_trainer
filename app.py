"""Streamlit UI for practicing multiplication tables."""

from __future__ import annotations

from typing import List, Optional

import streamlit as st

from memory_trainer import MultiplicationQuiz

NUM_QUESTIONS = 10


def _reset_quiz() -> None:
    """Replace the active quiz with a fresh one and clear answers."""

    st.session_state.quiz = MultiplicationQuiz.generate(NUM_QUESTIONS)
    st.session_state.pop("score", None)
    for index in range(NUM_QUESTIONS):
        st.session_state.pop(f"answer_{index}", None)


def _extract_answers(num_questions: int) -> List[Optional[int]]:
    """Retrieve answers from ``st.session_state`` and coerce them to integers."""

    answers: List[Optional[int]] = []
    for index in range(num_questions):
        raw_value = st.session_state.get(f"answer_{index}", "")
        try:
            answers.append(int(raw_value))
        except (TypeError, ValueError):
            answers.append(None)
    return answers


def main() -> None:
    st.title("Trening tabliczki mnożenia")
    st.write(
        "Odpowiedz na 10 pytań dotyczących mnożenia liczb z zakresu 2-12, "
        "a następnie sprawdź swój wynik."
    )

    if "quiz" not in st.session_state:
        _reset_quiz()

    quiz: MultiplicationQuiz = st.session_state.quiz

    with st.form("multiplication_quiz"):
        for index, question in enumerate(quiz.questions):
            st.text_input(
                label=f"Pytanie {index + 1}: {question.left} × {question.right} =",
                key=f"answer_{index}",
            )
        submitted = st.form_submit_button("Sprawdź odpowiedzi")

    if submitted:
        answers = _extract_answers(len(quiz.questions))
        st.session_state.score = quiz.grade(answers)

    if "score" in st.session_state:
        correct, total = st.session_state.score
        st.success(f"Twój wynik: {correct}/{total}")

    if st.button("Nowy zestaw pytań"):
        _reset_quiz()


if __name__ == "__main__":
    main()

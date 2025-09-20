"""Streamlit UI for practicing multiplication tables."""

from __future__ import annotations

import streamlit as st

from memory_trainer import MultiplicationQuiz

NUM_QUESTIONS = 10


def _reset_quiz() -> None:
    """Replace the active quiz with a fresh one and clear answers."""

    st.session_state.quiz = MultiplicationQuiz.generate(NUM_QUESTIONS)
    st.session_state.answers = [None] * len(st.session_state.quiz.questions)
    st.session_state.current_index = 0
    st.session_state.current_answer = ""
    st.session_state.pop("score", None)


def main() -> None:
    st.title("Trening tabliczki mnożenia")
    st.write(
        "Odpowiedz na 10 pytań dotyczących mnożenia liczb z zakresu 2-12. "
        "Po wpisaniu odpowiedzi pojawi się kolejne pytanie, a po ostatnim zobaczysz swój wynik."
    )

    if "quiz" not in st.session_state:
        _reset_quiz()

    quiz: MultiplicationQuiz = st.session_state.quiz

    if "answers" not in st.session_state or len(st.session_state.answers) != len(
        quiz.questions
    ):
        st.session_state.answers = [None] * len(quiz.questions)

    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    if "current_answer" not in st.session_state:
        st.session_state.current_answer = ""

    current_index = st.session_state.current_index

    if current_index < len(quiz.questions):
        question = quiz.questions[current_index]
        st.write(f"Pytanie {current_index + 1} z {len(quiz.questions)}")
        with st.form("current_question"):
            answer = st.text_input(
                label=f"{question.left} × {question.right} =",
                key="current_answer",
            )
            button_label = (
                "Następne pytanie"
                if current_index < len(quiz.questions) - 1
                else "Zakończ quiz"
            )
            submitted = st.form_submit_button(button_label)

        if submitted:
            try:
                st.session_state.answers[current_index] = int(answer)
            except (TypeError, ValueError):
                st.session_state.answers[current_index] = None

            st.session_state.current_index = current_index + 1
            st.session_state.current_answer = ""

            if st.session_state.current_index == len(quiz.questions):
                st.session_state.score = quiz.grade(st.session_state.answers)
            else:
                st.session_state.pop("score", None)
    elif "score" not in st.session_state:
        st.session_state.score = quiz.grade(st.session_state.answers)

    if "score" in st.session_state:
        correct, total = st.session_state.score
        st.success(f"Twój wynik: {correct}/{total}")

    if st.button("Nowy zestaw pytań"):
        _reset_quiz()


if __name__ == "__main__":
    main()

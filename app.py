"""Streamlit UI for practicing multiplication tables."""

from __future__ import annotations

from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

from memory_trainer import MultiplicationQuiz

NUM_QUESTIONS = 10


def _reset_quiz() -> None:
    """Replace the active quiz with a fresh one and clear answers."""

    st.session_state.quiz = MultiplicationQuiz.generate(NUM_QUESTIONS)
    st.session_state.answers = [None] * len(st.session_state.quiz.questions)
    st.session_state.current_index = 0
    st.session_state.current_answer = ""
    st.session_state.pop("score", None)


def _parse_answer(raw_answer: Optional[str]) -> Optional[int]:
    """Convert the raw answer text to an integer or ``None``."""

    if raw_answer is None:
        return None

    stripped = raw_answer.strip()
    if not stripped:
        return None

    try:
        return int(stripped)
    except ValueError:
        return None


def _submit_current_answer() -> None:
    """Store the current answer and advance to the next question."""

    if "quiz" not in st.session_state:
        return

    quiz: MultiplicationQuiz = st.session_state.quiz
    current_index: int = st.session_state.current_index

    if current_index >= len(quiz.questions):
        return

    current_answer_text: str = st.session_state.get("current_answer", "")
    st.session_state.answers[current_index] = _parse_answer(current_answer_text)
    st.session_state.current_index = current_index + 1
    st.session_state.current_answer = ""

    if st.session_state.current_index == len(quiz.questions):
        st.session_state.score = quiz.grade(st.session_state.answers)
    else:
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
        st.text_input(
            label=f"{question.left} × {question.right} =",
            key="current_answer",
            on_change=_submit_current_answer,
        )

        button_label = "Sprawdź wynik"
        if st.button(button_label):
            _submit_current_answer()

        components.html(
            """
            <script>
            const streamlitDoc = window.parent.document;
            const textInputs = streamlitDoc.querySelectorAll('input[type="text"]');
            if (textInputs.length > 0) {
                const answerInput = textInputs[textInputs.length - 1];
                answerInput.focus();
                const valueLength = answerInput.value.length;
                answerInput.setSelectionRange(valueLength, valueLength);
            }
            </script>
            """,
            height=0,
        )
    elif "score" not in st.session_state:
        st.session_state.score = quiz.grade(st.session_state.answers)

    answered_count = min(st.session_state.current_index, len(quiz.questions))
    if answered_count:
        st.subheader("Twoje odpowiedzi")
        for index in range(answered_count):
            question = quiz.questions[index]
            response = st.session_state.answers[index]
            correct_answer = question.answer

            if response == correct_answer:
                st.write(
                    f"✅ {question.left} × {question.right} = {correct_answer}"
                )
            else:
                if response is None:
                    response_text = "brak odpowiedzi"
                else:
                    response_text = str(response)

                st.write(
                    "❌ "
                    f"{question.left} × {question.right} = {response_text} "
                    f"- poprawna odpowiedź: {correct_answer}"
                )

    if "score" in st.session_state:
        correct, total = st.session_state.score
        st.success(f"{correct}/{total}")

    if st.button("Nowy zestaw pytań"):
        _reset_quiz()


if __name__ == "__main__":
    main()

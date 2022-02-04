from typing import (
    List,
    Tuple
)
import pytest
from durdle.durdle import check_guess

CORRECT: List[Tuple[str, str, Tuple[str, str]]] = [
    (
        "hello",
        "world",
        (
            "⬜ ⬜ ⬜ 🟩 🟨",
            ":regional_indicator_h: :regional_indicator_e: :regional_indicator_l: :regional_indicator_l: :regional_indicator_o:"
        )
    ),
    (
        "tests",
        "reefs",
        (
            "⬜ 🟩 ⬜ ⬜ 🟩",
            ":regional_indicator_t: :regional_indicator_e: :regional_indicator_s: :regional_indicator_t: :regional_indicator_s:"
        )
    ),
    (
        "dorea",
        "adore",
        (
            "🟨 🟨 🟨 🟨 🟨",
            ":regional_indicator_d: :regional_indicator_o: :regional_indicator_r: :regional_indicator_e: :regional_indicator_a:"
        )
    ),
    (
        "queen",
        "queen",
        (
            "🟩 🟩 🟩 🟩 🟩",
            ":regional_indicator_q: :regional_indicator_u: :regional_indicator_e: :regional_indicator_e: :regional_indicator_n:"
        )
    )
]
INCORRECT: List[Tuple[str, str, Tuple[str, str]]] = [
    (
        "hello",
        "aloha",
        (
            "⬜ ⬜ ⬜ 🟩 🟨",
            ":regional_indicator_h: :regional_indicator_e: :regional_indicator_l: :regional_indicator_l: :regional_indicator_o:"
        )
    ),
    (
        "tests",
        "thief",
        (
            "⬜ 🟩 ⬜ ⬜ 🟩",
            ":regional_indicator_t: :regional_indicator_e: :regional_indicator_s: :regional_indicator_t: :regional_indicator_s:"
        )
    ),
    (
        "adore",
        "adorn",
        (
            "🟨 🟨 🟨 🟨 🟨",
            ":regional_indicator_a: :regional_indicator_d: :regional_indicator_o: :regional_indicator_r: :regional_indicator_e:"
        )
    ),
    (
        "queen",
        "prince",
        (
            "🟩 🟩 🟩 🟩 🟩",
            ":regional_indicator_q: :regional_indicator_u: :regional_indicator_e: :regional_indicator_e: :regional_indicator_n:"
        )
    )
]

@pytest.mark.parametrize("guess, word, result", CORRECT)
def test_check_guess_correct(
    guess: str,
    word: str,
    result: Tuple[str, ...]
) -> None:
    data: Tuple[str, ...] = check_guess(guess, word)
    assert result == data

@pytest.mark.parametrize("guess, word, result", INCORRECT)
def test_check_guess_incorrect(
    guess: str,
    word: str,
    result: Tuple[str, ...]
) -> None:
    data: Tuple[str, ...] = check_guess(guess, word)
    assert result != data

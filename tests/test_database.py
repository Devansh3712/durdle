from typing import Tuple
from durdle.database import (
    get_word,
    get_user_streak
)

def test_get_word():
    word_data: Tuple[str, ...] = get_word()
    assert type(word_data) == tuple
    assert len(word_data) == 3
    assert len(word_data[0]) == 5

def test_get_user_streak():
    data: Tuple[int, ...] = get_user_streak("pytest")
    assert data[0] == 0
    assert data[1] == 0

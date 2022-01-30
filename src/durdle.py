from collections import Counter
from typing import (
    List,
    Dict,
    Tuple
)

emojis: Dict[int, str] = {
    0: "⬜",
    1: "🟩",
    2: "🟨"
}
letters: Dict[str, str] = {
    "a": ":regional_indicator_a:",
    "b": ":regional_indicator_b:",
    "c": ":regional_indicator_c:",
    "d": ":regional_indicator_d:",
    "e": ":regional_indicator_e:",
    "f": ":regional_indicator_f:",
    "g": ":regional_indicator_g:",
    "h": ":regional_indicator_h:",
    "i": ":regional_indicator_i:",
    "j": ":regional_indicator_j:",
    "k": ":regional_indicator_k:",
    "l": ":regional_indicator_l:",
    "m": ":regional_indicator_m:",
    "n": ":regional_indicator_n:",
    "o": ":regional_indicator_o:",
    "p": ":regional_indicator_p:",
    "q": ":regional_indicator_q:",
    "r": ":regional_indicator_r:",
    "s": ":regional_indicator_s:",
    "t": ":regional_indicator_t:",
    "u": ":regional_indicator_u:",
    "v": ":regional_indicator_v:",
    "w": ":regional_indicator_w:",
    "x": ":regional_indicator_x:",
    "y": ":regional_indicator_y:",
    "z": ":regional_indicator_z:"
}

def check_guess(guess: str, word: str) -> Tuple[str, str]:
    guess = guess.lower()
    result_emojis: str = ""
    result_string: str = " ".join([letters[char] for char in guess])
    chars: List[int] = []
    guess_dict: Dict[str, int] = dict(Counter(guess))
    word_dict: Dict[str, int] = dict(Counter(word))
    for idx in range(5):
        if guess[idx] == word[idx]:
            chars.append(1)
            word_dict[word[idx]] -= 1
            guess_dict[guess[idx]] -= 1
        elif guess[idx] in word:
            if guess_dict[guess[idx]] == word_dict[guess[idx]]:
                chars.append(2)
            elif guess_dict[guess[idx]] > word_dict[guess[idx]]:
                if word_dict[guess[idx]] != 0:
                    chars.append(2)
                    word_dict[guess[idx]] -= 1
                else:
                    chars.append(0)
            else:
                if guess_dict[guess[idx]] != 0:
                    chars.append(2)
                    guess_dict[guess[idx]] -= 1
                else:
                    chars.append(0)
        else:
            chars.append(0)
    for char in chars:
        result_emojis += emojis[char] + " "
    return (result_emojis[:-1], result_string)

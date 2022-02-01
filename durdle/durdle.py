from collections import Counter
import requests
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
    """Check a user's guess with the actual word.
    
    If a character in guessed word and the actual word is
    at the correct spot, 🟩 is added to the result, else
    if a character in guessed word is present in the actual
    word but at the wrong spot, 🟨 is added to the result else
    ⬜ is added to the result.

    Args:
        guess (str): Word guessed by the user.
        word (str): Word generated for the user.

    Returns:
        Tuple[str, str]: Tuple of result_emojis and emojified
        character string of guessed word.
    """
    guess = guess.lower()
    result_emojis: str = ""
    result_string: str = " ".join([letters[char] for char in guess])
    chars: List[int] = []
    guess_dict: Dict[str, int] = dict(Counter(guess))
    word_dict: Dict[str, int] = dict(Counter(word))
    for i, j in zip(guess, word):
        if i == j:
            chars.append(1)
            guess_dict[i] -= 1
            word_dict[j] -= 1
        else:
            chars.append(0)
    for idx in range(5):
        if chars[idx] != 1 and (guess[idx] in word) and word_dict[guess[idx]] != 0:
            if guess_dict[guess[idx]] == word_dict[guess[idx]]:
                chars[idx] = 2
                word_dict[guess[idx]] -= 1
                guess_dict[guess[idx]] -= 1
            elif guess_dict[guess[idx]] > word_dict[guess[idx]]:
                if word_dict[guess[idx]] != 0:
                    chars[idx] = 2
                    word_dict[guess[idx]] -= 1
                    guess_dict[guess[idx]] -= 1
                else:
                    chars[idx] = 0
                    guess_dict[guess[idx]] -= 1
            elif guess_dict[guess[idx]] < word_dict[guess[idx]]:
                if guess_dict[guess[idx]] != 0:
                    chars[idx] = 2
                    word_dict[guess[idx]] -= 1
                    guess_dict[guess[idx]] -= 1
                else:
                    chars[idx] = 0
                    guess_dict[guess[idx]] -= 1
            else:
                chars[idx] = 0
    for char in chars:
        result_emojis += emojis[char] + " "
    return (result_emojis[:-1], result_string)

def get_word_meaning(word: str):
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        data = requests.get(url).json()
        meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
        usage = data[0]["meanings"][0]["definitions"][0]["example"]
        return (meaning.capitalize(), usage.capitalize())
    except:
        return (False, False)

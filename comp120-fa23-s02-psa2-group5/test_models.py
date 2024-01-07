import pytest

from models import NotAWordError, LetterState, WordyModel

def test_check_guess_correct():
    model = WordyModel(4, 'long_wordlist.txt', preselected_word="help")

    expected_letter_states = [LetterState.CORRECT] * 4
    expected_key_states = {'h': LetterState.CORRECT,
                           'e': LetterState.CORRECT,
                           'l': LetterState.CORRECT,
                           'p': LetterState.CORRECT}

    is_correct, letter_states, key_states = model.check_guess("help")
    assert is_correct, "Wrong result (answer and guess are both 'help')"
    assert letter_states == expected_letter_states, "Incorrect letter states"
    assert key_states == expected_key_states, "Incorrect key states"

def test_check_guess_all_incorrect():
    model = WordyModel(4, 'long_wordlist.txt', preselected_word="help")

    expected_letter_states = [LetterState.INCORRECT] * 4
    expected_key_states = {'k': LetterState.INCORRECT,
                           'n': LetterState.INCORRECT,
                           'o': LetterState.INCORRECT,
                           't': LetterState.INCORRECT}

    is_correct, letter_states, key_states = model.check_guess("knot")
    assert not is_correct, "Wrong result"
    assert letter_states == expected_letter_states, "Incorrect letter states"
    assert key_states == expected_key_states, "Incorrect key states"

def test_check_guess_one_correct():
    model = WordyModel(4, 'long_wordlist.txt', preselected_word="help")

    expected_letter_states = [LetterState.CORRECT, LetterState.INCORRECT, LetterState.INCORRECT, LetterState.INCORRECT]
    expected_key_states = {'h': LetterState.CORRECT,
                           'a': LetterState.INCORRECT,
                           'c': LetterState.INCORRECT,
                           'k': LetterState.INCORRECT}

    is_correct, letter_states, key_states = model.check_guess("hack")
    assert not is_correct, "Wrong result"
    assert letter_states == expected_letter_states, "Incorrect letter states"
    assert key_states == expected_key_states, "Incorrect key states"

def test_check_guess_one_misplaced():
    model = WordyModel(4, 'long_wordlist.txt', preselected_word="help")

    expected_letter_states = [LetterState.INCORRECT, LetterState.INCORRECT, LetterState.INCORRECT, LetterState.MISPLACED]
    expected_key_states = {'h': LetterState.MISPLACED,
                           'c': LetterState.INCORRECT,
                           'a': LetterState.INCORRECT,
                           's': LetterState.INCORRECT}

    is_correct, letter_states, key_states = model.check_guess("cash")
    assert not is_correct, "Wrong result"
    assert letter_states == expected_letter_states, "Incorrect letter states"
    assert key_states == expected_key_states, "Incorrect key states"

def test_check_guess_correct_plus_misplaced():
    model = WordyModel(4, 'long_wordlist.txt', preselected_word="help")

    expected_letter_states = [LetterState.MISPLACED, LetterState.CORRECT, LetterState.INCORRECT, LetterState.INCORRECT]
    expected_key_states = {'p': LetterState.MISPLACED,
                           'e': LetterState.CORRECT,
                           'a': LetterState.INCORRECT,
                           't': LetterState.INCORRECT}

    is_correct, letter_states, key_states = model.check_guess("peat")
    assert not is_correct, "Wrong result"
    assert letter_states == expected_letter_states, "Incorrect letter states"
    assert key_states == expected_key_states, "Incorrect key states"

def test_check_guess_repeated_letters_one_correct_one_incorrect():
    model = WordyModel(4, 'long_wordlist.txt', preselected_word="stop")

    expected_letter_states = [LetterState.CORRECT, LetterState.INCORRECT, LetterState.INCORRECT, LetterState.INCORRECT]
    expected_key_states = {'s': LetterState.CORRECT,
                           'i': LetterState.INCORRECT,
                           'n': LetterState.INCORRECT}

    is_correct, letter_states, key_states = model.check_guess("sins")
    assert not is_correct, "Wrong result"
    assert letter_states == expected_letter_states, "Incorrect letter states"
    assert key_states == expected_key_states, "Incorrect key states"

def test_check_guess_repeated_letters_one_correct_one_incorrect():
    model = WordyModel(4, 'long_wordlist.txt', preselected_word="sits")

    expected_letter_states = [LetterState.INCORRECT, LetterState.INCORRECT, LetterState.MISPLACED, LetterState.CORRECT]
    expected_key_states = {'m': LetterState.INCORRECT,
                           'e': LetterState.INCORRECT,
                           's': LetterState.CORRECT}

    is_correct, letter_states, key_states = model.check_guess("mess")
    assert not is_correct, "Wrong result"
    assert letter_states == expected_letter_states, "Incorrect letter states"
    assert key_states == expected_key_states, "Incorrect key states"

def test_check_guess_raises_notaword_exception():
    model = WordyModel(4, 'long_wordlist.txt')

    with pytest.raises(NotAWordError):
        model.check_guess("fftz")


if __name__ == "__main__":
    pytest.main()

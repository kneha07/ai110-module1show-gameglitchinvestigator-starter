# tests/test_game_logic.py
from logic_utils import check_guess, update_score, parse_guess, get_range_for_difficulty


def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_hints_not_backwards():
    # Before fix: guess 33 with secret 22 incorrectly said "Go HIGHER!"
    outcome, message = check_guess(33, 22)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_correct_guess_always_wins():
    outcome, _ = check_guess(42, 42)
    assert outcome == "Win"

    # --- New Tests: Edge Cases & Validation ---

def test_parse_guess_invalid():
    """Verify that non-numeric strings don't crash the game."""
    ok, value, err = parse_guess("apple")
    assert ok is False
    assert value is None
    assert "not a number" in err.lower()

def test_parse_guess_decimal():
    """Verify the game handles decimal inputs by rounding/converting."""
    ok, value, err = parse_guess("55.5")
    assert ok is True
    assert value == 55

def test_score_minimum_floor():
    """Verify that a win always awards at least 10 points (no negative wins)."""
    # 100 - 10 * (15 + 1) = -60, but our logic should floor it at 10.
    new_score = update_score(current_score=100, outcome="Win", attempt_number=15)
    assert new_score == 110  # 100 (base) + 10 (floor)

def test_difficulty_ranges():
    """Verify that the range settings correctly adjust to difficulty."""
    low_e, high_e = get_range_for_difficulty("Easy")
    assert high_e == 20
    
    low_h, high_h = get_range_for_difficulty("Hard")
    assert high_h == 50
import random
import streamlit as st
# FIX: All logic moved to logic_utils.py
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮", layout="wide")
st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

# --- CHALLENGE 4: SIDEBAR ENHANCEMENTS ---
st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)

attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

st.sidebar.divider()
st.sidebar.subheader("📊 Guess History")

# Initialize session state
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts" not in st.session_state:
    st.session_state.attempts = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "status" not in st.session_state:
    st.session_state.status = "playing"
if "history" not in st.session_state:
    st.session_state.history = []

# Challenge 4: Sidebar History Table
if st.session_state.history:
    st.sidebar.table(st.session_state.history)
else:
    st.sidebar.write("No guesses yet!")

# --- CHALLENGE 4: DASHBOARD METRICS ---
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Score", st.session_state.score)
col_m2.metric("Attempt", f"{st.session_state.attempts} / {attempt_limit}")
col_m3.metric("Difficulty", difficulty)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.subheader("Make a guess")
raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀", use_container_width=True)
with col2:
    new_game = st.button("New Game 🔁", use_container_width=True)
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: Resets all session state so game starts completely fresh
if new_game:
    st.session_state.attempts = 1
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success(f"🏆 You already won! Final score: {st.session_state.score}")
    else:
        st.error(f"💀 Game over! The secret was {st.session_state.secret}.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)
    if not ok:
        st.session_state.history.append({"Guess": raw_guess, "Result": "❌ Invalid"})
        st.error(f"🚫 {err}")
    else:
        outcome, message = check_guess(guess_int, st.session_state.secret)
        
        # Challenge 4: Proximity Logic (Hot/Cold)
        diff = abs(guess_int - st.session_state.secret)
        emoji = "🔥" if diff <= 5 else "❄️"
        
        # Update history for sidebar table
        st.session_state.history.append({"Guess": guess_int, "Result": f"{emoji} {outcome}"})

        if show_hint:
            # Challenge 4: Color-coded hint boxes
            if outcome == "Win":
                st.success(message)
            else:
                st.warning(f"{emoji} {message}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )
        
        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(f"You won! The secret was {st.session_state.secret}. Final score: {st.session_state.score}")
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(f"Out of attempts! The secret was {st.session_state.secret}. Score: {st.session_state.score}")
            else:
                st.session_state.attempts += 1

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
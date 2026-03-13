# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

The first time I ran it, the game looked fine — a clean UI with a text input, a submit button, and a hint section. It wasn't until I started actually playing that things got weird. The hints were sending me the wrong way, my score was changing in ways that made no sense, and clicking New Game didn't really reset anything.

- List at least two concrete bugs you noticed at the start  
 
Bug 1: The hints pointed the wrong way
The hints were telling me the wrong thing. When the secret was 22 and I guessed 33, it said "Go HIGHER!" — but I should have gone lower. The game knew my guess was wrong but pointed me in the opposite direction every single time.

Bug 2: No range validation
I typed 0, -1, and 100000000000000 — all accepted without any warning. Only numbers within low to high should be allowed.

Bug 3:The "New Game" button didn't actually start a new game
When I clicked "New Game" after winning or losing, the game stayed locked. The secret changed but the score, history, and game status never reset — so it immediately showed "You already won" or "Game over" again before I could even guess.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Claude (claude.ai)  and Copilot as my  AI tool on this project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

One thing Claude got right was identifying that the hint messages in check_guess were swapped — it pointed directly to the lines where "Go HIGHER!" and "Go LOWER!" were attached to the wrong outcomes. I verified this by playing the game myself and confirming that every hint pointed the wrong way.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

One thing Claude missed was the range validation bug — it gave me a list of 8 bugs but never flagged that typing 0, -1, or 100000000000000 was accepted without any warning. I found it myself by testing edge cases while playing, and also noticed that invalid inputs like nnnn were still being saved to the guess history even after being rejected.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I decided a bug was really fixed when I could reproduce the exact scenario that broke it and get the correct result this time. For the hints bug, I played the game manually — I opened the debug panel, noted the secret, guessed a number I knew was too high, and confirmed the hint now said "Go LOWER!" instead of "Go HIGHER!" For the New Game bug, I manually won a game, clicked New Game, and verified the score reset to 0 and I could guess immediately without getting blocked.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  I ran pytest with PYTHONPATH=. pytest tests/ and got 5 passed in 0.01s. The most useful test was test_hints_not_backwards — it called check_guess(33, 22) and checked that the outcome was "Too High" and the message contained "LOWER". Before the fix that test would have failed because the message said "Go HIGHER!" instead.

- Did AI help you design or understand any tests? How?
Claude helped me understand that check_guess returns a tuple, not just a string — so the tests needed to unpack both values like outcome, message = check_guess(...) instead of comparing the whole result to just "Too Low". That was the reason my first test run failed, and fixing that made all 5 tests pass.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
The secret felt like it kept changing because on even-numbered attempts the code converted it to a string, so 42 == "42" returned False even when the guess was exactly right.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit reruns the whole script on every button click, so without session state every variable would reset on each interaction — session state acts like a notepad that keeps things like the secret and score stable across those reruns.

- What change did you make that finally gave the game a stable secret number?
The fix was removing the str() conversion so the comparison was always int vs int, and resetting all session state keys when New Game was clicked so the game started completely fresh.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
One habit I want to carry into future projects is writing sanity check tests before trusting AI-generated logic — even one pytest covering the happy path would have caught the backwards hints immediately. If I had written assert check_guess(80, 42) == ("Too High", "📉 Go LOWER!") on day one, the bug would have failed loudly instead of hiding in plain sight. I also want to keep using Git commits after each individual fix rather than committing everything at once — it made it easy to see exactly what changed and why at each step.


- What is one thing you would do differently next time you work with AI on a coding task?
Next time I work with AI on a coding task, I would ask it to explain why a specific line exists before accepting it — the str() conversion on even attempts had no clear purpose, and questioning it earlier would have flagged it as a bug much faster.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
This project changed how I think about AI-generated code — I used to assume that if code runs without crashing it's probably correct, but silent logic errors like wrong hints are harder to catch than exceptions and need a human to actually play the game and think critically.

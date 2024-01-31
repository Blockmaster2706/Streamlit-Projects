import streamlit as st
import random

# make a word array that is every fruit in the world
words = ["apple", "banana", "cherry", "durian", "elderberry", "fig", "grape", "honeydew", "imbe", "jackfruit", "kiwi", "lime", "mango", "nectarine", "orange", "papaya", "quince", "raspberry", "strawberry", "tangerine", "ugli", "vanilla", "watermelon", "xigua", "yuzu", "zucchini"]

if "word" not in st.session_state.keys():
    st.session_state["word"] = random.choice(words)
    st.session_state["guessed"] = []
    st.session_state["tries"] = 7
    st.session_state["state"] = "playing"

word = st.session_state["word"]
guessed = st.session_state["guessed"]
tries = st.session_state["tries"]

# display number of tries
st.write("Number of tries: ", tries)

# write the current word, replacing all unguessed letters with an underscore
display_word = " ".join([i if i in guessed else "_" for i in word])
st.write(display_word)

# give a selection box for all letters that have not yet been guessed
guess = st.selectbox("Select a letter", [i for i in "abcdefghijklmnopqrstuvwxyz" if i not in guessed])

# give a reset button next to the guess button
if st.button("Reset"):
    st.session_state["word"] = random.choice(words)
    st.session_state["guessed"] = []
    st.session_state["tries"] = 7
    st.session_state["state"] = "playing"

    st.rerun()

if st.button("Guess!") & (st.session_state["state"] == "playing"):

    guessed.append(guess)

    if guess in word:
        st.write("Correct!")
    else:
        st.write("Incorrect!")
        st.session_state["tries"] -= 1

    st.rerun()

if "_" not in display_word:
    st.write("You win!")
    st.session_state["state"] = "won"
    st.stop()

if tries == 0:
    st.write("You lose!")
    st.session_state["state"] = "lost"
    st.stop()
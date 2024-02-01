import streamlit as st
import random
   
st.write('''<style>
[data-testid="column"] {
    width: calc(10% - 1rem) !important;
    flex: 1 1 calc(10% - 1rem) !important;
    min-width: calc(10% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)

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

# guessed letters
guessed_letters_string: str = ""
    
for i in guessed:
    guessed_letters_string += i + ", "

if guessed_letters_string.endswith(", "):
    guessed_letters_string = guessed_letters_string[:-2]

st.write("Guessed letters: ", guessed_letters_string)

# write the current word, replacing all unguessed letters with an underscore
display_word = " ".join([i if i in guessed else "_" for i in word])

if display_word[0] == "_":
    display_word = "\\" + display_word

st.write(display_word)

availableletters = lambda: [i for i in "abcdefghijklmnopqrstuvwxyz" if i not in guessed]
# give a selection box for all letters that have not yet been guessed

guess = ""

def make_up_to_10_buttons(letters: list):
    
    col: list = st.columns(10)

    for i in range(letters.__len__()):
        if col.__len__() > i:
            with col[i]:
                if col[i].button(letters[i]):
                    if st.session_state["state"] == "playing":

                        guessed.append(letters[i])

                        if letters[i] in word:
                            st.write("Correct!")
                        else:
                            st.write("Incorrect!")
                            st.session_state["tries"] -= 1

                        st.rerun()

letters_to_show: list = availableletters()

while letters_to_show.__len__() > 0:
    while letters_to_show.__len__() > 0:
        letters: list = []

        for i in range(10):
            if letters_to_show.__len__() > 0:
                letters.append(letters_to_show[0])
                letters_to_show.pop(0)
            if letters_to_show is None: break
        make_up_to_10_buttons(letters)
        
        if letters_to_show is None: break

        
        
button_cols = st.columns(4)

# give a reset button next to the guess button
with button_cols[0]:
    if st.button("Reset"):
        st.session_state["word"] = random.choice(words)
        st.session_state["guessed"] = []
        st.session_state["tries"] = 7
        st.session_state["state"] = "playing"

        st.rerun()

with button_cols[1]:
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
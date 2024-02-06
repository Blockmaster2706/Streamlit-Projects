import streamlit as st
import random
import time
import base64
   
def Reset():
    st.session_state["word"] = random.choice(get_wordlist())
    st.session_state["guessed"] = []
    st.session_state["tries"] = 7
    st.session_state["state"] = "playing"
    st.session_state["input_word"] = ""
    st.session_state.input = ""
    st.rerun()

def list_callback():
    st.session_state["old_list"] = st.session_state["selected_list"]
    st.session_state["selected_list"] = st.session_state.new_list

def Solve():
    input = st.session_state["input_word"]
    if input == word:
        for i in input.lower():
            if i not in guessed:
                guessed.append(i)
                guessed.append(i.upper())
    elif input != "":
        st.session_state["tries"] -= 1

st.write('''<style>
[data-testid="column"] {
    width: calc(10% - 1rem) !important;
    flex: 1 1 calc(10% - 1rem) !important;
    min-width: calc(10% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)

if "selected_list" not in st.session_state.keys():
    st.session_state["selected_list"] = "Fruits"

def get_wordlist():
    match st.session_state["selected_list"]:
    # make a word array that is every fruit in the world
        case "Fruits":
            return ["apple", "banana", "cherry", "durian", "elderberry", "fig", "grape", "honeydew", "imbe", "jackfruit", "kiwi", "lime", "mango", "nectarine", "orange", "papaya", "quince", "raspberry", "strawberry", "tangerine", "ugli", "vanilla", "watermelon", "xigua", "yuzu", "zucchini"]
        case "Hazbin Hotel":
            return ['Tom Trench', 'Vaggie', 'Lilith', 'Charlie', 'Vox', 'Molly', 'Sir Pentious', 'Lucifer', 'Alastor', 'Cherri Bomb', 'Velvet', 'Angel Dust', 'Niffty', 'Fat Nuggets', 'Valentino', 'Razzle and Dazzle', 'Katie Killjoy', 'Husk', 'Egg Bois', 'Rosie']

if "word" not in st.session_state.keys():
    st.session_state["word"] = random.choice(get_wordlist())
    st.session_state["guessed"] = []
    st.session_state["tries"] = 7
    st.session_state["state"] = "playing"
    st.session_state["selected_list"] = "Fruits"
    st.session_state["input_word"] = ""

word = st.session_state["word"]
guessed = st.session_state["guessed"]
tries = st.session_state["tries"]

# display number of tries
st.write("Number of tries: ", tries)

# guessed letters
guessed_letters_string: str = ""
guessed_letters_to_show: set = set()

for i in guessed:
    guessed_letters_to_show.add(i.upper())

for i in sorted(guessed_letters_to_show):
    guessed_letters_string += i + ", "

if guessed_letters_string.endswith(", "):
    guessed_letters_string = guessed_letters_string[:-2]

st.write("Guessed letters: ", guessed_letters_string)

# write the current word, replacing all unguessed letters with an underscore
display_word = ""

for i in word:
    if i in guessed:
        display_word += i
    elif i == " ":
        display_word += " | "
    else:
        display_word += "_ "

if display_word[0] == "_":
    display_word = "\\" + display_word

wordcols = st.columns(2)

with wordcols[0]:
    st.write(display_word)
with wordcols[1]:
    options = ["Fruits", "Hazbin Hotel"]
    selected_list = st.selectbox("Selected Wordlist", options, label_visibility="collapsed", key="new_list", index=options.index(st.session_state["selected_list"]))
    if st.session_state["selected_list"] != selected_list:
        st.session_state["selected_list"] = selected_list
        Reset()

availableletters = lambda: [i for i in "abcdefghijklmnopqrstuvwxyz" if i not in guessed]
# give a selection box for all letters that have not yet been guessed

def make_up_to_10_buttons(letters: list):
    
    col: list = st.columns(10)

    for i in range(letters.__len__()):
        if col.__len__() > i:
            with col[i]:
                if col[i].button(letters[i]):
                    if st.session_state["state"] == "playing":

                        guessed.append(letters[i])
                        guessed.append(letters[i].upper())

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

columns: list = st.columns([1, 1, 8])

# give a reset button next to the guess button
with columns[0]:
    if st.button("Reset"):
        Reset()

        st.rerun()
with columns[1]:
    st.write("Solve:")
with columns[2]:
    st.session_state["input_word"] = st.text_input("Word to solve for", key="input", label_visibility="collapsed", on_change=Solve())

if "_" not in display_word:
    st.write("You win!")
    st.session_state["state"] = "won"
    st.stop()

if tries == 0:
    st.write("You lose! The Word was: " + word)
    st.session_state["state"] = "lost"

    file_ = open("./HangmanImages/YouLose.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
    )
    st.stop()


import streamlit as st
import random
import time
import base64
from streamlit_autorefresh import st_autorefresh
import socket
import json

st_autorefresh(interval=100000)

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 65432
        self.addr = (self.server, self.port)
        self.session_state = json.loads(self.connect())

    def connect(self):
        try:
            self.client.connect(self.addr)
            data = self.client.recv(10240).decode()

            return data
        except Exception as e:
            print(e)
            return "Error"

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            data = self.client.recv(10240).decode()

            return data
        except socket.error as e:
            print(e)



st.write('''<style>
[data-testid="column"] {
    width: calc(10% - 1rem) !important;
    flex: 1 1 calc(10% - 1rem) !important;
    min-width: calc(10% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)

if "word" not in st.session_state.keys():

    st.session_state["network"] = Network()

state = st.session_state["network"].session_state
print(state)

st.session_state["word"] = state["word"]
st.session_state["guessed"] = state["guessed"] if state["guessed"] is not None else list()
st.session_state["tries"] = state["tries"]
st.session_state["state"] = state["state"]
st.session_state["input_word"] = state["input_word"]

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

st.write(display_word)

availableletters = lambda: [i for i in "abcdefghijklmnopqrstuvwxyz" if i not in guessed]
# give a selection box for all letters that have not yet been guessed

def make_up_to_10_buttons(letters: list):
    
    col: list = st.columns(10)

    for i in range(letters.__len__()):
        if col.__len__() > i:
            with col[i]:
                if col[i].button(letters[i]):
                    if st.session_state["state"] == "playing":

                        global state
                        state = json.loads(st.session_state["network"].send(letters[i]))
                        st.session_state["network"].session_state = state


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

columns: list = st.columns([2, 8])

def Solve(input: str):
    if input == word and st.session_state["state"] == "playing":
        for i in input.lower():
            if i not in guessed:
                guessed.append(i)
                guessed.append(i.upper())
        st.rerun()
    elif input != "":
        st.session_state["tries"] -= 1

# give a reset button next to the guess button
with columns[0]:
    st.text_input("Word to solve for", key="input", label_visibility="collapsed")
with columns[1]:
    if st.button("Solve"):
        Solve(st.session_state.input)

if "_" not in display_word:
    st.write("You win!")
    st.session_state["state"] = "won"

    stage = abs(tries - 9)

    file_ = open("./HangmanImages/{}Win.gif".format(stage), "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
    )

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

if tries < 9 and "_" in display_word:
    st.image("./HangmanImages/{}.png".format(abs(tries - 8)))
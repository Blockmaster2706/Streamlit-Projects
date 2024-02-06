import sys
import socket
import selectors
import types
import random
import json
import keyboard
from _thread import *

session_state = {
    "selected_list": "",
    "word": "",
    "guessed": list(),
    "tries": 9,
    "state": "playing",
    "input_word": ""
}

def get_wordlist():
    match session_state["selected_list"]:
    # make a word array that is every fruit in the world
        case "Fruits":
            return ["apple", "banana", "cherry", "durian", "elderberry", "fig", "grape", "honeydew", "imbe", "jackfruit", "kiwi", "lime", "mango", "nectarine", "orange", "papaya", "quince", "raspberry", "strawberry", "tangerine", "ugli", "vanilla", "watermelon", "xigua", "yuzu", "zucchini"]
        case "Hazbin Hotel":
            return ['Tom Trench', 'Vaggie', 'Lilith', 'Charlie', 'Vox', 'Molly', 'Sir Pentious', 'Lucifer', 'Alastor', 'Cherri Bomb', 'Velvet', 'Angel Dust', 'Niffty', 'Fat Nuggets', 'Valentino', 'Razzle and Dazzle', 'Katie Killjoy', 'Husk', 'Egg Bois', 'Rosie']

session_state["selected_list"] = "Fruits"
session_state["word"] = random.choice(get_wordlist())

server = "127.0.0.1"
port = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

def get_guess(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def guess(str):
    global session_state
    session_state["guessed"].append(str)
    session_state["guessed"].append(str.upper())

    if str not in session_state["word"]:
        session_state["tries"] -= 1

def threaded_client(conn):
    print(conn.send(str.encode(json.dumps(session_state))))
    
    while True:
            data = conn.recv(10240).decode()
            print(data)
            guess(data)

            if not data:
                print("Disconnected")
                break
            else:
                reply = json.dumps(session_state)

                print("Received: ", data)
                print("Sending : ", str.encode(json.dumps(session_state)))

            print(reply)
            conn.sendall(str.encode(json.dumps(session_state)))

    print("Lost connection")
    conn.close()

def reset_game():
    while True:
        if keyboard.is_pressed("ctrl+r"):
            global session_state 
            session_state = {
                "selected_list": "",
                "word": "",
                "guessed": list(),
                "tries": 9,
                "state": "playing",
                "input_word": ""
            }
            print("Reset Game")
start_new_thread(reset_game, ())

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, tuple([conn]))
    currentPlayer += 1
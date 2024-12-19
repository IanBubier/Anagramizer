from english_words import get_english_words_set
from random import shuffle
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:7070")

english_dictionary = get_english_words_set(['gcide'], alpha=True, lower=True)

while True:
    message = socket.recv_string()
    try:
        request = json.loads(message)
        if request == 'quit':
            reply = json.dumps('Ending Process.')
            socket.send_string(reply)
            break
        elif type(request) is not dict or len(request) != 2:
            reply = 'Invalid Message Format'
        else:
            try:
                if request['meaning'] == 'meaningful' or request['meaning'] == 'meaningless':
                    word = request['word']
                    char_list = []
                    for char in word:
                        char_list.append(char)
                    shuffle(char_list)
                    anagram = ''
                    for char in char_list:
                        anagram += char
                    if request['meaning'] == 'meaningful':
                        while anagram not in english_dictionary or anagram == word:
                            char_list = []
                            for char in anagram:
                                char_list.append(char)
                            shuffle(char_list)
                            anagram = ''
                            for char in char_list:
                                anagram += char
                    else:
                        while anagram in english_dictionary or anagram == word:
                            char_list = []
                            for char in anagram:
                                char_list.append(char)
                            shuffle(char_list)
                            anagram = ''
                            for char in char_list:
                                anagram += char
                    print(word, anagram, word == anagram)
                    print(anagram in english_dictionary)
                    reply = anagram
                else:
                    reply = 'Invalid Meaning Value'
            except KeyError:
                reply = 'KeyError'
    except json.JSONDecodeError:
        reply = 'JSONDecodeError'
    socket.send_string(json.dumps(reply))

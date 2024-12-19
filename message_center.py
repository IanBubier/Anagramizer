import zmq
import json

context = zmq.Context()

anagramizer_ui_socket = context.socket(zmq.REP)
anagramizer_ui_socket.bind("tcp://*:6060")

anagram_finder_socket = context.socket(zmq.REQ)
anagram_finder_socket.connect("tcp://localhost:7070")

anagram_storage_socket = context.socket(zmq.REQ)
anagram_storage_socket.connect("tcp://localhost:24686")

user_storage_socket = context.socket(zmq.REQ)
user_storage_socket.connect("tcp://localhost:13579")

string2dictionary_socket = context.socket(zmq.REQ)
string2dictionary_socket.connect("tcp://localhost:5555")

while True:
    message = anagramizer_ui_socket.recv_string()
    try:
        request = json.loads(message)
        if request == 'quit':
            reply = json.dumps('Ending Process.')
            anagramizer_ui_socket.send_string(reply)
            break
        elif type(request) is not dict or len(request) != 2:
            reply = json.dumps('Invalid Message Format')
        else:
            try:
                forward = json.dumps(request['content'])
                if request['destination'] == 'anagram_finder':
                    anagram_finder_socket.send_string(forward)
                    reply = anagram_finder_socket.recv_string()
                elif request['destination'] == 'anagram_storage':
                    anagram_storage_socket.send_string(forward)
                    reply = anagram_storage_socket.recv_string()
                elif request['destination'] == 'user_storage':
                    user_storage_socket.send_string(forward)
                    reply = user_storage_socket.recv_string()
                elif request['destination'] == 'string2dictionary':
                    string2dictionary_socket.send_string(forward)
                    reply = string2dictionary_socket.recv_string()
                else:
                    reply = json.dumps('Invalid Destination')
            except KeyError:
                reply = json.dumps('KeyError')
    except json.JSONDecodeError:
        reply = json.dumps('JSONDecodeError')
    anagramizer_ui_socket.send_string(reply)

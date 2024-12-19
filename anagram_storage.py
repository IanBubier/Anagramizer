import json
import zmq
from pathlib import Path

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:24686')


def store_anagram(characters, meaning, anagram):
    if Path(f'Anagrams/{meaning}/{characters}.json').is_file() is False:
        Path(f'Anagrams/{meaning}/{characters}.json').touch(exist_ok=False)
        with open(f'Anagrams/{meaning}/{characters}.json', 'w') as outfile:
            json.dump([], outfile)
    try:
        with open(f'Anagrams/{meaning}/{characters}.json', 'r') as infile:
            anagrams = json.load(infile)
            if anagram not in anagrams:
                anagrams.append(anagram)
                anagrams.sort()
        with open(f'Anagrams/{meaning}/{characters}.json', 'w') as outfile:
            json.dump(anagrams, outfile)
        func_return = f'{characters} anagrams updated.'
    except FileNotFoundError:
        func_return = 'FileNotFoundError'
    except PermissionError:
        func_return = 'PermissionError'
    return func_return


def read_anagrams(characters, meaning):
    try:
        with open(f'Anagrams/{meaning}/{characters}.json', 'r') as infile:
            anagrams = json.load(infile)
        func_return = anagrams
    except FileNotFoundError:
        func_return = 'FileNotFoundError'
    except PermissionError:
        func_return = 'PermissionError'
    return func_return


if __name__ == '__main__':
    while True:
        message = socket.recv_string()
        try:
            request = json.loads(message)
            if request == 'quit':
                reply = json.dumps('Ending Process.')
                socket.send_string(reply)
                break
            elif type(request) is not dict or len(request) != 4:
                reply = 'Invalid Message Format'
            else:
                try:
                    operation = request['operation']
                    characters = request['characters']
                    anagram = request['anagram']
                    meaning = request['meaning']
                    if type(operation) is not str:
                        reply = 'Invalid Operation Format'
                    elif type(characters) is not str:
                        reply = 'Invalid Characters Format'
                    elif type(anagram) is not str and anagram is not None:
                        reply = 'Invalid Anagram Format'
                    elif type(meaning) is not str:
                        reply = 'Invalid Meaning Format'
                    else:
                        if operation != 'store' and operation != 'read':
                            reply = 'Invalid Operation String'
                        elif meaning != 'meaningful' and meaning != 'meaningless':
                            reply = 'Invalid Meaning String'
                        elif operation == 'store':
                            reply = store_anagram(characters, meaning, anagram)
                        else:
                            reply = read_anagrams(characters, meaning)
                except KeyError:
                    reply = 'KeyError'
                except ValueError:
                    reply = 'ValueError'
        except json.JSONDecodeError:
            reply = 'JSONDecodeError'
        socket.send_string(json.dumps(reply))

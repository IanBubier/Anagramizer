import json
import zmq
from pathlib import Path

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:13579')


def create_account(account):
    try:
        Path(f'Favorites/{account}.json').touch(exist_ok=False)
        with open(f'Favorites/{account}.json', 'w') as outfile:
            json.dump([], outfile)
        func_return = f'{account} created.'
    except FileExistsError:
        func_return = 'FileExistsError'
    return func_return


def check_account(account):
    if Path(f'Favorites/{account}.json').exists() is True:
        func_return = 'exists'
    else:
        func_return = 'none'
    return func_return


def delete_account(account):
    try:
        Path(f'Favorites/{account}.json').unlink()
        func_return = f'{account} deleted.'
    except FileNotFoundError:
        func_return = 'FileNotFoundError'
    except PermissionError:
        func_return = 'PermissionError'
    return func_return


def add_favorite(account, favorite):
    try:
        with open(f'Favorites/{account}.json', 'r') as infile:
            favorites = json.load(infile)
            favorites.append(favorite)
            favorites.sort()
        with open(f'Favorites/{account}.json', 'w') as outfile:
            json.dump(favorites, outfile)
        func_return = f'{account} favorites updated.'
    except FileNotFoundError:
        func_return = 'FileNotFoundError'
    except PermissionError:
        func_return = 'PermissionError'
    return func_return


def remove_favorite(account, favorite):
    try:
        with open(f'Favorites/{account}.json', 'r') as infile:
            favorites = json.load(infile)
            favorites.remove(favorite)
        with open(f'Favorites/{account}.json', 'w') as outfile:
            json.dump(favorites, outfile)
        func_return = f'{account} favorites updated.'
    except FileNotFoundError:
        func_return = 'FileNotFoundError'
    except PermissionError:
        func_return = 'PermissionError'
    except ValueError:
        func_return = 'ValueError'
    return func_return


def read_favorites(account):
    try:
        with open(f'Favorites/{account}.json', 'r') as infile:
            favorites = json.load(infile)
        func_return = favorites
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
            elif type(request) is not dict or len(request) != 3:
                reply = 'Invalid Message Format'
            else:
                try:
                    operation = request['operation']
                    account = request['account']
                    anagram = request['anagram']
                    if type(operation) is not str:
                        reply = 'Invalid Operation Format'
                    elif type(account) is not str:
                        reply = 'Invalid Characters Format'
                    elif type(anagram) is not str and anagram is not None:
                        reply = 'Invalid Anagram Format'
                    else:
                        valid_ops = ['create', 'check', 'delete', 'add', 'remove', 'read']
                        if operation not in valid_ops:
                            reply = 'Invalid Operation String'
                        elif operation == 'create':
                            reply = create_account(account)
                        elif operation == 'check':
                            reply = check_account(account)
                        elif operation == 'delete':
                            reply = delete_account(account)
                        elif operation == 'add':
                            reply = add_favorite(account, anagram)
                        elif operation == 'remove':
                            reply = remove_favorite(account, anagram)
                        else:
                            reply = read_favorites(account)
                except KeyError:
                    reply = 'KeyError'
        except json.JSONDecodeError:
            reply = 'JSONDecodeError'
        socket.send_string(json.dumps(reply))

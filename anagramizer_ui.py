import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:6060")

print("\nWelcome to the Anagramizer!")
exit_input = False
while exit_input is False:
    user_name = None
    user_input = input("\nPlease enter a profile name to continue, NEW PROFILE to create a new profile, "
                       "or EXIT to exit the program. ")
    if user_input == "EXIT":
        print("\nThank you for using the Anagramizer!\n")
        break
    elif user_input == "NEW PROFILE":
        user_input = input("\nPlease enter your new profile name. ")
        content = {'operation': 'create', 'account': user_input, 'anagram': None}
        message = json.dumps({'destination': 'user_storage', 'content': content})
        socket.send_string(message)
        socket.recv_string()
        user_name = user_input
    else:
        content = {'operation': 'check', 'account': user_input, 'anagram': None}
        message = json.dumps({'destination': 'user_storage', 'content': content})
        socket.send_string(message)
        response = json.loads(socket.recv_string())
        if response == 'exists':
            user_name = user_input
        else:
            print("\nProfile Name Not Recognized")

    while user_name is not None:
        menu_input = input("\nPlease enter ANAGRAM to proceed to anagram generation, PROFILE to return to the profile "
                           "menu, LOAD to view your saved anagrams, DELETE to delete this account, EXIT to exit the "
                           "program, or any other string of English characters to generate a meaningful anagram. ")

        if menu_input == "ANAGRAM":
            meaning_value = input("\nWould you like your generated anagram to be meaningful within the English "
                                  "language? Please enter YES or NO. ")
            while meaning_value != 'YES' and meaning_value != 'NO':
                meaning_value = input("\nInvalid input. Would you like your anagram to be meaningful within the English"
                                      " language? Please enter YES or NO. ")
            if meaning_value == 'YES':
                meaning_value = 'meaningful'
            else:
                meaning_value = 'meaningless'
            letter_string = input(
                "\nPlease enter a string of English letters. The Anagramizer will print a list of words "
                "that can be made with the letters in that string. You will then have the option to save "
                "the string for future recall. ")
            content = {'string': letter_string}
            message = json.dumps({'destination': 'string2dictionary', 'content': content})
            socket.send_string(message)
            count = json.loads(socket.recv_string())
            if count['word_frequency'] is None:
                print("\nInvalid Characters Detected")
            else:
                content = {'word': letter_string, 'meaning': meaning_value}
                message = json.dumps({'destination': 'anagram_finder', 'content': content})
                socket.send_string(message)
                anagram = json.loads(socket.recv_string())
                characters = ""
                character_list = []
                for character in count['character_frequency']:
                    character_list.append(character)
                    character_list.sort()
                for character in character_list:
                    characters += str(character)
                    characters += str(count['character_frequency'][character])
                content = {'operation': 'store', 'characters': characters, 'meaning': meaning_value, 'anagram': anagram}
                message = json.dumps({'destination': 'anagram_storage', 'content': content})
                socket.send_string(message)
                socket.recv_string()
                save_input = input(
                    f"\nYour string {letter_string} can make the word: {anagram}. Enter SAVE to save this combination "
                    f"or any other key to continue. ")
                if save_input == "SAVE":
                    content = {'operation': 'add', 'account': user_name, 'anagram': f'{letter_string} - {anagram}'}
                    message = json.dumps({'destination': 'user_storage', 'content': content})
                    socket.send_string(message)
                    socket.recv_string()
                    print(f"\nSaved string {anagram} to your profile.")
                all_input = input(f"\nEnter ALL to view all {meaning_value} anagrams discovered for {menu_input} or "
                                  f"any other key to return to the menu. ")
                if all_input == "ALL":
                    content = {'operation': 'read', 'characters': characters, 'meaning': meaning_value, 'anagram': None}
                    message = json.dumps({'destination': 'anagram_storage', 'content': content})
                    socket.send_string(message)
                    reply = json.loads(socket.recv_string())
                    print(f"\nThese are all anagrams discovered for {letter_string}:")
                    for anagram in reply:
                        print(anagram)

        elif menu_input == "PROFILE":
            break

        elif menu_input == "LOAD":
            content = {'operation': 'read', 'account': user_name, 'anagram': None}
            message = json.dumps({'destination': 'user_storage', 'content': content})
            socket.send_string(message)
            reply = json.loads(socket.recv_string())
            print(f"\nThese are your saved anagrams:")
            for pair in reply:
                print(pair)
            delete_input = input("\nEnter a word - anagram pair to delete it from your saved anagrams or any other key "
                                 "to continue. ")
            if delete_input in reply:
                content = {'operation': 'remove', 'account': user_name, 'anagram': delete_input}
                message = json.dumps({'destination': 'user_storage', 'content': content})
                socket.send_string(message)
                reply = json.loads(socket.recv_string())
            print(f'\n{delete_input} removed from your saved anagrams.')

        elif menu_input == "DELETE":
            content = {'operation': 'delete', 'account': user_name, 'anagram': None}
            message = json.dumps({'destination': 'user_storage', 'content': content})
            socket.send_string(message)
            socket.recv_string()
            print(f"\n{user_name} account deleted.")
            user_name = None

        elif menu_input == "EXIT":
            print("\nThank you for using the Anagramizer!\n")
            exit_input = True
            break

        else:
            content = {'string': menu_input}
            message = json.dumps({'destination': 'string2dictionary', 'content': content})
            socket.send_string(message)
            count = json.loads(socket.recv_string())
            if count['word_frequency'] is None:
                print("\nInvalid Characters Detected")
            else:
                content = {'word': menu_input, 'meaning': 'meaningful'}
                message = json.dumps({'destination': 'anagram_finder', 'content': content})
                socket.send_string(message)
                anagram = json.loads(socket.recv_string())
                characters = ""
                character_list = []
                for character in count['character_frequency']:
                    character_list.append(character)
                    character_list.sort()
                for character in character_list:
                    characters += str(character)
                    characters += str(count['character_frequency'][character])
                content = {'operation': 'store', 'characters': characters, 'meaning': 'meaningful', 'anagram': anagram}
                message = json.dumps({'destination': 'anagram_storage', 'content': content})
                socket.send_string(message)
                socket.recv_string()
                save_input = input(
                    f"\nYour string {menu_input} can make the word: {anagram}. Enter SAVE to save this combination or "
                    f"any other key to continue.")
                if save_input == "SAVE":
                    content = {'operation': 'add', 'account': user_name, 'anagram': f'{menu_input} - {anagram}'}
                    message = json.dumps({'destination': 'user_storage', 'content': content})
                    socket.send_string(message)
                    socket.recv_string()
                    print(f"\nSaved string {anagram} to your profile.")
                all_input = input(f"\nEnter ALL to view all meaningful anagrams discovered for {menu_input} or any "
                                  f"other key to return to the menu. ")
                if all_input == "ALL":
                    content = {'operation': 'read', 'characters': characters, 'meaning': 'meaningful', 'anagram': None}
                    message = json.dumps({'destination': 'anagram_storage', 'content': content})
                    socket.send_string(message)
                    reply = json.loads(socket.recv_string())
                    print(f"\nThese are all anagrams discovered for {menu_input}:")
                    for anagram in reply:
                        print(anagram)

message = json.dumps({'destination': 'anagram_finder', 'content': 'quit'})
socket.send_string(message)
socket.recv_string()
message = json.dumps({'destination': 'anagram_storage', 'content': 'quit'})
socket.send_string(message)
socket.recv_string()
message = json.dumps({'destination': 'user_storage', 'content': 'quit'})
socket.send_string(message)
socket.recv_string()
message = json.dumps('quit')
socket.send_string(message)
socket.recv_string()

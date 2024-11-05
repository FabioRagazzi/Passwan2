import os
import json


def get_index(my_list, element):
    return my_list.index(element)


def increment_string(num_str):
    num = int(num_str)+1
    return str(num % 10)


def decrement_string(num_str):
    num = int(num_str)-1
    if num == -1:
        num = 9
    return str(num)


def read_json_file(file_path, default_value):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # Parse JSON data
    except json.JSONDecodeError:
        data = default_value
    except FileNotFoundError:
        data = default_value
        with open(file_path, 'w') as _:
            pass
    return data


def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def id_num_to_str(n):
    id_num_str = str(n)
    return id_num_str.zfill(3)


def text_to_state(text):
    full_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f",
                 "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
                 "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                 "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "`", "~",
                 "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=", "{", "}",
                 "[", "]", "|", ":", ";", "'", "<", ">", ",", ".", "?", "/"]
    # initializing output
    output_state = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]

    # converting text to ASCII value
    for j in range(4):
        for i in range(4):
            output_state[i][j] = full_list.index(text[4*j + i])

    return output_state


def state_to_text(state_in, char_list):
    # initializing output
    text_out = ""

    # converting to text using only the characters
    # present in char_list
    list_length = len(char_list)
    for j in range(4):
        for i in range(4):
            text_out += char_list[state_in[i][j] % list_length]

    return text_out


def add_to_clipboard(text_to_add):
    with open("temp.txt", "w") as file:
        file.write(text_to_add.strip())
    os.system("clip < temp.txt")
    os.remove("temp.txt")

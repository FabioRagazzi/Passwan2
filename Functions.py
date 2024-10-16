import os
import json
from Work_in_json_mode import *

# You can specify here the path of the .ico file that will be the icon of your application
PATH_TO_ICON = "passwan2.ico"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# DO NOT MODIFY UNDER HERE !!!!
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


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
        with open(PATH_OF_DATA+file_path, 'r') as file:
            data = json.load(file)  # Parse JSON data
    except json.JSONDecodeError:
        data = default_value
    except FileNotFoundError:
        data = default_value
        with open(PATH_OF_DATA+file_path, 'w') as _:
            pass
    return data


def write_json_file(file_path, data):
    with open(PATH_OF_DATA+file_path, 'w') as file:
        json.dump(data, file, indent=4)


def id_num_to_str(n):
    id_num_str = str(n)
    return id_num_str.zfill(3)


def text_to_state(text):
    # initializing output
    output_state = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]

    # converting text to ASCII value
    for j in range(4):
        for i in range(4):
            output_state[i][j] = ord(text[4 * j + i])

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

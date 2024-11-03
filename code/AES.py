from AES_data import SUBBYTES, INV_SUBBYTES, RCON, MIXCOL, INV_MIXCOL


def subbyte(n):
    j = n & 0x0F
    i = n >> 4
    return SUBBYTES[i][j]


def inv_subbyte(n):
    j = n & 0x0F
    i = n >> 4
    return INV_SUBBYTES[i][j]


def state_subbyte(state_in):
    output_state = state_in.copy()
    for i in range(4):
        for j in range(4):
            output_state[i][j] = subbyte(output_state[i][j])
    return output_state


def back_state_subbyte(state_in):
    output_state = state_in.copy()
    for i in range(4):
        for j in range(4):
            output_state[i][j] = inv_subbyte(output_state[i][j])
    return output_state


def gf_mult(a, b):
    p = 0
    while a != 0 and b != 0:
        if b & 1:
            p ^= a
        if a & 0x80:
            a = (a << 1) ^ 0x11b
        else:
            a <<= 1
        b >>= 1
    return p


def shift_rows(state_in):
    value_saved1 = state_in[1][0]
    state_in[1][0] = state_in[1][1]
    state_in[1][1] = state_in[1][2]
    state_in[1][2] = state_in[1][3]
    state_in[1][3] = value_saved1

    value_saved1 = state_in[2][0]
    value_saved2 = state_in[2][1]
    state_in[2][0] = state_in[2][2]
    state_in[2][1] = state_in[2][3]
    state_in[2][2] = value_saved1
    state_in[2][3] = value_saved2

    value_saved1 = state_in[3][3]
    state_in[3][3] = state_in[3][2]
    state_in[3][2] = state_in[3][1]
    state_in[3][1] = state_in[3][0]
    state_in[3][0] = value_saved1


def back_shift_rows(state_in):
    value_saved1 = state_in[1][3]
    state_in[1][3] = state_in[1][2]
    state_in[1][2] = state_in[1][1]
    state_in[1][1] = state_in[1][0]
    state_in[1][0] = value_saved1

    value_saved1 = state_in[2][0]
    value_saved2 = state_in[2][1]
    state_in[2][0] = state_in[2][2]
    state_in[2][1] = state_in[2][3]
    state_in[2][2] = value_saved1
    state_in[2][3] = value_saved2

    value_saved1 = state_in[3][0]
    state_in[3][0] = state_in[3][1]
    state_in[3][1] = state_in[3][2]
    state_in[3][2] = state_in[3][3]
    state_in[3][3] = value_saved1


def mix_columns(state_in):
    # initializing output
    output_state = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]

    # computing galois field matrix product
    for i in range(4):
        for j in range(4):
            new_value = 0x0
            for k in range(4):
                new_value = new_value ^ gf_mult(MIXCOL[i][k], state_in[k][j])
            output_state[i][j] = new_value

    return output_state


def back_mix_columns(state_in):
    # initializing output
    output_state = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]

    # computing galois field matrix product
    for i in range(4):
        for j in range(4):
            new_value = 0x0
            for k in range(4):
                new_value = new_value ^ gf_mult(INV_MIXCOL[i][k], state_in[k][j])
            output_state[i][j] = new_value

    return output_state


def xor(state_in, key):
    output_state = state_in.copy()
    for i in range(4):
        for j in range(4):
            output_state[i][j] = state_in[i][j] ^ key[i][j]
    return output_state


def next_key(key_in, rcon):
    # initializing output
    output_key = [[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]

    # storing columns
    col_1 = [key_in[0][0], key_in[1][0], key_in[2][0], key_in[3][0]]
    col_2 = [key_in[0][1], key_in[1][1], key_in[2][1], key_in[3][1]]
    col_3 = [key_in[0][2], key_in[1][2], key_in[2][2], key_in[3][2]]
    col_4 = [key_in[0][3], key_in[1][3], key_in[2][3], key_in[3][3]]
    new_col = col_4.copy()

    # shifting last column
    value_saved = new_col[0]
    new_col[0] = new_col[1]
    new_col[1] = new_col[2]
    new_col[2] = new_col[3]
    new_col[3] = value_saved

    # substituting last column
    for i in range(4):
        new_col[i] = subbyte(new_col[i])

    # XOR with rcon and 1st column
    for i in range(4):
        output_key[i][0] = new_col[i] ^ col_1[i]
    output_key[0][0] = output_key[0][0] ^ rcon

    # computing 2nd column of new key
    for i in range(4):
        output_key[i][1] = output_key[i][0] ^ col_2[i]

    # computing 3rd column of new key
    for i in range(4):
        output_key[i][2] = output_key[i][1] ^ col_3[i]

    # computing 4th column of new key
    for i in range(4):
        output_key[i][3] = output_key[i][2] ^ col_4[i]

    return output_key


def expand_key(key_in):
    key_list = [key_in]
    for i in range(10):
        key_list.append(next_key(key_list[i], RCON[i]))
    return key_list


def crypt(message_in, key_in):
    key_list = expand_key(key_in)

    state = xor(message_in, key_list[0])
    for i in range(1, 11):
        state = state_subbyte(state)
        shift_rows(state)
        if i != 10:
            state = mix_columns(state)
        state = xor(state, key_list[i])
    return state


def decrypt(cipher_text, key_in):
    key_list = expand_key(key_in)

    state = xor(cipher_text, key_list[10])
    for i in range(9, -1, -1):
        back_shift_rows(state)
        state = back_state_subbyte(state)
        state = xor(state, key_list[i])
        if i != 0:
            state = back_mix_columns(state)
    return state


def print_state(state_in):
    dummy_state = state_in.copy()
    for i in range(4):
        for j in range(4):
            print(hex(dummy_state[i][j]), end=" \t")
        print("")

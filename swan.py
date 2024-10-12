from AES import *

key = [[0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0],
       [0x0a, 0, 0, 0]]

message = [[0, 0, 0, 0xff],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

print_state(crypt(message, key))

# The output should be:
# 0x83 	 0xa3 	 0x26 	 0x6a
# 0xf7 	 0xa1 	 0x3c 	 0xcf
# 0x86 	 0x13 	 0x9c 	 0xe1
# 0x8d 	 0xe5 	 0xb8 	 0x80

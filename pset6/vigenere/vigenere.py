# Ruchella Kock
# 12460796
# This program will take an alphabetical key which will cipher a text the user fills in

import sys
from cs50 import get_string


def cipher(each_character, each_key_character, y):
    """
    enciphers each character of a string
    """
    alphabetical_cipher = ((ord(each_key_character.lower()) - 97) + (ord(each_character) - y)) % 26
    cipher_character = chr(alphabetical_cipher + y)
    print(f"{cipher_character}", end="")


def main():
    # program will not run if it doesnt get 2 command line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: vigenere.py key")

    # check if there is an integer in the key
    key = sys.argv[1]
    if not key.isalpha():
        sys.exit("Usage: vigenere.py alphabetical key")

    # prompt user for text
    plain_text = get_string("plaintext: ")
    print("ciphertext: ", end="")

    A, a, j = 65, 97, 0
    length_key = len(key)
    # go over every character of the string and execute cipher accordingly
    for character in plain_text:
        each_key_character = key[j % length_key]
        if character.isupper():
            cipher(character, each_key_character, A)
            j = j + 1
        elif character.islower():
            cipher(character, each_key_character, a)
            j = j + 1
        else:
            print(f"{character}", end="")
    print()


if __name__ == "__main__":
    main()
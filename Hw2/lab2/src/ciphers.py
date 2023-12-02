"""
CSCI-603 Lab 2: Ciphers

A program that encodes/decodes a message by applying a set of transformation operations.
The transformation operations are:
    shift - Sa[,n] changes letter at index a by moving it n letters fwd in the alphabet. A negative
        value for n shifts the letter backward in the alphabet.
    rotate - R[n] rotates the string n positions to the right. A negative value for n rotates the string
        to the left.
    duplicate - Da[,n] follows character at index a with n copies of itself.
    trade - Ta,b swap the places of the a-th and b-th characters.
    affine - Aa,b applies the affine cipher algorithm y = (ax + b) mod 26 using a and b as keys.

All indices number (the subscript parameters) are 0-based.

author: Prateek Sharma
"""


def shift(msg: str, index: int, exponent: int) -> str:
    """
    shift - Sa[,n] changes letter at index a by moving it n letters fwd in the alphabet. A negative
        value for n shifts the letter backward in the alphabet.
    :param msg: word on which the transformation to be applied
    :param index: index of the letter in the word on which the transformation is applied
    :param exponent: number of times to be applied
    :return:
    """
    # assuming the msg will always be upper case
    exponent = exponent % 26
    if ord(msg[index]) + exponent > 90:
        return (
            msg[:index]
            + chr(ord("A") + exponent + ord(msg[index]) - 91)
            + msg[index + 1 :]
        )
    return msg[:index] + chr(ord(msg[index]) + exponent) + msg[index + 1 :]


def rotate(msg: str, exponent: int) -> str:
    """
    function rotates the string n positions to the right. A negative value for n rotates the string
        to the left.
    :param msg: text string on which transformation need to be applied
    :param exponent: how many times it needs to be rotated
    :return: transformed string
    """
    exponent = exponent % len(msg)
    return msg[-exponent:] + msg[:-exponent]


def duplicate(msg: str, index: int, exponent: int) -> str:
    """
    function follows character at index with n copies of itself.
    :param msg:text string on which transformation need to be applied
    :param index: which letter in the string needs to be duplicated
    :param exponent: how many times it needs to be duplicated
    :return: transformed string
    """
    return msg[:index] + msg[index] * exponent + msg[index:]


def de_duplicate(msg: str, index: int, exponent: int) -> str:
    """
    function follows character at index a and removed the duplicated character for n number of times
    :param msg: text string on which transformation need to be applied
    :param index: position which need to be de duplicated, 'a'
    :param exponent: number of times to be de duplicated 'n'
    :return: transformed string
    """
    return msg[:index] + msg[index + exponent :]


def trade(msg: str, index_1: int, index_2: int) -> str:
    """
    trade - Ta,b swap the places of the a-th and b-th characters.
    :param msg:text string on which transformation need to be applied
    :param index_1: 'a' index of the first number
    :param index_2: 'b' index of the second number
    :return:transformed string
    """
    index_2 = index_2 % len(msg)
    index_1 = index_1 % len(msg)
    return (
        msg[:index_1]
        + msg[index_2]
        + msg[index_1 + 1 : index_2]
        + msg[index_1]
        + msg[index_2 + 1 :]
    )


def encrypt_affine(msg: str, a: int, b: int) -> str:
    """
    affine - Aa,b applies the affine cipher algorithm for encryption y = (ax + b) mod 26 using a and b as keys.
    :param msg:text string on which transformation need to be applied
    :param a: keys provided by user
    :param b: keys provided by user
    :return:transformed string
    """
    new_msg = ""
    for letter in msg:
        ord_letter = ord(letter) - ord("A")
        new_msg += chr(ord("A") + (a * ord_letter + b) % 26)
    return new_msg


def decrypt_affine(msg: str, a: int, b: int) -> str:
    """
    Aa,b applies the affine cipher algorithm for decryption y = a-1(x - b) mod 26 using a and b as keys.
    :param msg:text string on which transformation need to be applied
    :param a: modular inverse of key provided by user
    :param b: key provided by user
    :return:transformed string
    """
    new_msg = ""
    for letter in msg:
        ord_letter = ord(letter) - ord("A")
        new_msg += chr(ord("A") + (a * (ord_letter - b)) % 26)
    return new_msg


def decode_cypher(cypher: str) -> []:
    """
    The function responsible for splitting the encryption string to different elements such as
    encryption algo to use and at what index as well as what exponent
    :param cypher: string contains the info which needs to be decoded
    :return: list where 1st element is transformation algo to use
    2nd index
    3rd exponent
    """
    cypher.strip()
    split_cypher = cypher.split(",")
    transformation = split_cypher[0][0]
    index = split_cypher[0][1:].strip()
    if index == "":
        index = 1
    exponent = 1
    if len(split_cypher) > 1:
        exponent = split_cypher[1].strip()
    return [transformation, int(index), int(exponent)]


def main() -> None:
    """
    The main loop responsible for getting the input details from the user
    and printing in the standard output the results
    of encrypting or decrypting the message applying the transformations
    :return: None
    """
    operation = ""
    while operation != "Q":
        operation = input("What do you want to do: (E)ncrypt, (D)ecrypt or (Q)uit? ")
        if operation == "Q":
            print("GOODBYE!")
        elif operation == "E" or operation == "D":
            msg = input("Enter the message: ")
            ciphers = input("Enter the encrypting transformation operations: ")
            print(
                "Generating output ...\n"
                + call_transformations_based_on_input(ciphers, msg, operation)
            )


def calculate_modular_multiplicative_inverse(a: int) -> int:
    """
    function calculates the modular multiplicative inverse of the given number a
    :param a: number for which the inverse needs to be found
    :return: inverse number
    """
    for i in range(1, 26):
        if (a * i) % 26 == 1:
            return i


def call_transformations_based_on_input(ciphers: str, msg: str, operation: str) -> str:
    """
    function to call the respective transformation functions based on the input by user
    :param ciphers: the text string for operation/s to perform
    :param msg: word on which it needs to be performed
    :param operation: encrypt or decrypt
    :return: encrypted/decrypted text string
    """
    if operation == "E":
        cypher_list = ciphers.split(";")
    else:
        cypher_list = ciphers.split(";")[::-1]
    for cypher in cypher_list:
        split_cypher = decode_cypher(cypher)
        if operation == "E":
            if split_cypher[0] == "S":
                msg = shift(msg, split_cypher[1], split_cypher[2])
            elif split_cypher[0] == "R":
                msg = rotate(msg, split_cypher[1])
            elif split_cypher[0] == "D":
                msg = duplicate(msg, split_cypher[1], split_cypher[2])
            elif split_cypher[0] == "T":
                msg = trade(msg, split_cypher[1], split_cypher[2])
            elif split_cypher[0] == "A":
                msg = encrypt_affine(msg, split_cypher[1], split_cypher[2])
        elif operation == "D":
            if split_cypher[0] == "S":
                msg = shift(msg, split_cypher[1], -split_cypher[2])
            elif split_cypher[0] == "R":
                msg = rotate(msg, -split_cypher[1])
            elif split_cypher[0] == "D":
                msg = de_duplicate(msg, split_cypher[1], split_cypher[2])
            elif split_cypher[0] == "T":
                msg = trade(msg, split_cypher[1], split_cypher[2])
            elif split_cypher[0] == "A":
                msg = decrypt_affine(
                    msg,
                    calculate_modular_multiplicative_inverse(split_cypher[1]),
                    split_cypher[2],
                )
    return msg


if __name__ == "__main__":
    main()

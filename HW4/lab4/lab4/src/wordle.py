from dataclasses import dataclass
import random
import sys
import re


marker_for_correct_word_in_correct_place = "^"
marker_for_correct_word_in_incorrect_place = "*"
legal_file_name = "../data/wordle.txt"  # put the legal file location here
data_file_name = "../data/wordle.txt"  # put the data file location here

welcome_text = """Commands:
    new: Start a new game
    guess <word>: Make a guess
    cheat: Show the secret word
    help: This help message
    quit: End the program
>"""


@dataclass
class Words:
    """
    Class to hold the word details
    current_word : the picked word to be guessed
    guessed_word : the word user entered
    list_of_guesses : list of tuples having the previous guesses and the markers
    num_of_guesses : hold the number of guesses that has happened till now
    guessed: flag if the word is guessed or not
    """

    current_word: str
    guessed_word: str
    list_of_guesses: list
    letters_used: set
    num_of_guesses: int
    guessed: bool


def get_random_word(set_of_words: set) -> str:
    """
    method to get random words from the set of words
    :param set_of_words: set of all the words read from file
    :return: word that will be used to play the game
    """
    index = random.randint(0, len(set_of_words) - 1)
    count = 0
    word = ""
    for x in set_of_words:
        if index == count:
            word = x
        count += 1
    set_of_words.remove(word)
    return word


def check_and_mark_word_positions(word: Words) -> list:
    """
    method to check and mark the guessed word with markers to show user which word is present and which is not
    :param word: object which contains all the info about the current and guessed word
    :return: list with the markers (*,^)
    """
    word.current_word = word.current_word.upper()
    word.guessed_word = word.guessed_word.upper()
    marker_list = [" " for _ in range(5)]
    output_list = [" " for _ in range(5)]
    # mark all the correct words ate correct positions
    for i in range(len(word.current_word)):
        word.letters_used.add(word.guessed_word[i])
        if word.current_word[i] == word.guessed_word[i]:
            output_list[i] = marker_for_correct_word_in_correct_place
            marker_list[i] = "t"  # traversed marker
    for i in range(len(word.current_word)):
        if output_list[i] == " ":
            for j in range(len(word.current_word)):
                if marker_list[j] == " ":
                    if word.guessed_word[i] == word.current_word[j]:
                        marker_list[j] = "t"
                        output_list[i] = marker_for_correct_word_in_incorrect_place
    return output_list


def process_output_and_update_object(output_list: list, word: Words):
    """
    method to check and display if the word is guessed or is yet to be guessed and updates it in the word object
    :param output_list: the list with markers in it
    :param word: object with all the info
    """
    marker = ""
    for i in output_list:
        marker += i
    if [marker_for_correct_word_in_correct_place for _ in range(5)] == output_list:
        word.list_of_guesses.append((word.guessed_word, marker))
        word.guessed = True
    else:
        word.list_of_guesses.append((word.guessed_word, marker))
    for i in word.list_of_guesses:
        print(i[0])
        print(i[1])
    print("Letters used: ", word.letters_used)


def present_in_legal_words(s: str) -> bool:
    """
    method to check if the word entered by user is present in the set of legal words or not
    :param s: word to be checked
    :return: True if found else False
    """

    if s.upper() in legal_words:
        return True
    return False


def guess(word: Words, s: str) -> str:
    """
    method to check if the input is valid or not and if valid calling the check method to validate and mark words
    :param word: object with all the data
    :param s: input word
    :return: string to be displayed
    """
    # print("input word", s)
    if not re.fullmatch("[a-z]{5}", s):
        return "Illegal word.\n>"
    elif not present_in_legal_words(s):
        return "Illegal word.\n>"
    else:
        word.num_of_guesses += 1
        word.guessed_word = s
        print("Num of guesses: ", word.num_of_guesses, " of 6")
        output_list = check_and_mark_word_positions(word)
        process_output_and_update_object(output_list, word)
        return ">"


def read_from_file(filename: str) -> set:
    """
    method to read data from the given file and populate it into a set
    :param filename: name of the file from which the data to be read
    :return: set of read values
    """
    set_of_words = set()
    with open(filename) as file_pointer:
        file_pointer.readline()  # comment if the first line not need to be discarded
        for line in file_pointer:
            set_of_words.add(line.strip())
    return set_of_words


legal_words = read_from_file(legal_file_name)  # set of all the legal word

# valid_commands = {"^new$", "^guess [a-z]{5}$", "^cheat$", "^help$", "^quit$"}


def main():
    """
    main method to call when the game to be started
    """
    print("Welcome to Wordle App!")
    word_passed = check_if_word_passed()
    # file of words
    set_of_words = read_from_file(data_file_name)
    process_commands(set_of_words, word_passed)


def process_commands(set_of_words: set, word_passed: str):
    """
    method used to process the input commands from the user such as new, quit
    the method will run infinitely until quit is been typed in the command line
    to start the game new has to be entered else game cannot be played
    :param set_of_words: set of all the word read from file
    :param word_passed: word chosen randomly or if the word is input from the command line
    """
    text = welcome_text
    game_on = True
    word = create_words_object(word_passed.upper() if (word_passed is not None) else "")
    while game_on:
        text, word = check_if_won_or_lost(text, word)
        user_input = input(text).lower()
        if user_input == "quit":
            game_on = False
        elif (
            re.search("^guess .+", user_input)
            and word.current_word != ""
            and word.current_word is not None
        ):
            text = guess(word, user_input.split(" ")[1])
        elif (
            user_input == "cheat"
            and word.current_word != ""
            and word.current_word is not None
        ):
            print("Secret word: " + word.current_word)
            text = ">"
        elif re.search("^guess .+", user_input) and (
            word.current_word is None or word.current_word == ""
        ):
            print("Start the game first be entering 'new' command")
            text = ">"
        elif user_input == "cheat" and (
            word.current_word is None or word.current_word == ""
        ):
            print("Start the game first be entering 'new' command")
            text = ">"
        elif user_input == "help":
            text = welcome_text
        elif user_input == "new":
            word = start_new_game(set_of_words)
            text = ">"
        else:
            print("Invalid command!")
            text = welcome_text


def check_if_won_or_lost(text: str, word: Words) -> (str, Words):
    """
    method validating if the number of try's are over 6 or if the word is guessed by user
    :param text: to be displayed on screen
    :param word: word object with all details
    :return: tuple with text and updated word object, if any
    """
    if word.guessed:
        print("You Won!!")
        text = ">"
        word = create_words_object("")
    elif word.num_of_guesses == 6:
        print("You Lost!!")
        print("The secret word was " + word.current_word)
        text = ">"
        word = create_words_object("")
    return text, word


def create_words_object(word: str) -> Words:
    """
    method to create a new object with default parameters and the word sent to it
    :param word: value to be stored in new words object
    :return: Words object with current word having value of the input parameter
    """
    return Words(
        current_word=word,
        guessed_word="",
        list_of_guesses=[],
        letters_used=set(),
        num_of_guesses=0,
        guessed=False,
    )


def start_new_game(set_of_words: set) -> Words:
    """
    method called when user enters new keyword in the cmd line
    and it checks if the run is for first time then it
    initializes the word with command line argument if provided
    else gets a random word from the set of words
        :param set_of_words: set of words read from input file
        :return: Words object with the word chosen as current word parameter
    """
    return create_words_object(get_random_word(set_of_words))


def check_if_word_passed() -> str:
    """
    method to check if in command line a word is passed or not and the input word as correct length or not
        :return: None if invalid or word
    """
    word_chosen = None
    if len(sys.argv) > 2:
        print("Usage: wordle [1st-secret-word]")
    elif (
        len(sys.argv) == 2
        and len(sys.argv[1]) == 5
        and re.fullmatch("[a-z]{5}", sys.argv[1].lower())
    ):
        word_chosen = sys.argv[1]
    elif len(sys.argv) != 1:
        print("Usage: wordle [1st-secret-word]")

    return word_chosen


if __name__ == "__main__":
    main()

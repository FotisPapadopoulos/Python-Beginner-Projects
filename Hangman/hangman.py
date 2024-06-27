# play the hangman
# you can add as many words you want in the list_of_words

from random import randrange

# globals
list_of_words = ["awkward", "nymph", "onyx", "ovary",
                 "oxidize", "oxygen", "pajama", "jiujitsu",
                 "nightclub", "galvanize", "yachtsman", "glowworm"]

max_rounds = 10  # if it is not possible to find the word in 10 rounds, the variable will increase to the minimum rounds


# needed to guess the word, of course you can change the number to whatever integer number you want


# functions
def print_word(hidden_word_tuple, word_found):
    print()
    cnt = 0
    for elm in hidden_word_tuple:
        print(elm[1], end="")
        if elm[1] == "_":
            cnt += 1
    else:
        if cnt == 0:
            word_found = True
    print()


def yes_or_no() -> str:
    user_input = input("Type 'yes' or 'no': ").strip().lower()
    while True:
        if user_input not in ["yes", "no"]:
            print("\nThis is not a valid answer.")
            user_input = input("Type 'yes' or 'no': ").strip().lower()
        else:
            return user_input


def main():
    round_cnt = 0

    global max_rounds

    hidden_word = list_of_words[randrange(len(list_of_words))].strip().lower()
    # print(hidden_word)

    if len(set(hidden_word)) > max_rounds > 0:
        max_rounds = len(set(hidden_word))

    hidden_word_tuple = tuple([[letter, "_"] for letter in hidden_word])
    # print(hidden_word_tuple)

    guessed_letters_list = []

    word_found = False
    print_word(hidden_word_tuple, word_found)

    word_guess_activated = False

    while max_rounds > 0:
        round_cnt += 1

        # check if player has lost all of his chances

        if round_cnt > max_rounds:
            print("You lost. Maximum rounds reached!!!")
            print(f"The hidden word is {hidden_word}.")
            break

        # get the guess letter from the user

        user_guess_letter = input(f"\nRound {round_cnt}/{max_rounds}. Write a letter: ").lower().strip()
        while True:
            if len(user_guess_letter) != 1:
                print("Only one letter please...")
                user_guess_letter = input(f"Round {round_cnt}/{max_rounds}. Write a letter: ").lower().strip()
            elif not user_guess_letter.isalpha():
                print("This is not a letter...")
                user_guess_letter = input(f"Round {round_cnt}/{max_rounds}. Write a letter: ").lower().strip()
            elif user_guess_letter in guessed_letters_list:
                print("You have already written this letter...")
                user_guess_letter = input(f"Round {round_cnt}/{max_rounds}. Write a letter: ").lower().strip()
            else:
                guessed_letters_list.append(user_guess_letter)
                break

        # print the found letters of the word

        cnt = 0
        for elm in hidden_word_tuple:
            if elm[0] == user_guess_letter:
                elm[1] = elm[0]
                cnt += 1

        print(f"Round {round_cnt}/{max_rounds}. The letter {user_guess_letter} exists {cnt} time / times in the word.")

        print_word(hidden_word_tuple, word_found)

        if word_found:
            print("Congratulations, you found the word!!!")
            break

        # guess the word at once

        print("\nDo you want to guess the word?")
        user_input = yes_or_no()

        if user_input == "yes":
            word_guess_activated = True

            user_input = input("\nType the word you think is the correct one: ").strip().lower()
            while not user_input.isalpha():
                print("\nSorry, only letters...")
                user_input = input("Type the word you think is the correct one: ").strip().lower()

            if user_input == hidden_word:
                print(f"\nThat's correct!!! The hidden word is: {hidden_word}")
            else:
                print(f"\nUnfortunately the guess is not correct... The hidden word is: {hidden_word}")

        if word_guess_activated:
            break


main()

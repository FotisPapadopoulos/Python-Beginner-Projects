# this is a program where 2 players play tic-tac-toe

from random import choice
from copy import deepcopy

# globals
box_status = [[" ", " ", " "],
              [" ", " ", " "],
              [" ", " ", " "]]

total_games = 10


# functions
def print_box(box_status:list):
    print()
    row_of_status = 0
    print("  " + "1".center(7) + "2".center(6) + "3".center(6))
    for row in range(7):
        if row % 2 == 0:
            print("  +-----+-----+-----+")
        else:
            print(f"{row_of_status + 1} |", end="")
            for column in range(3):
                value = box_status[row_of_status][column]
                print("  " + value + "  |", end="")
            print("")
            row_of_status += 1


# check user input
def check_if_int(string_for_input: str, start=None, end=None) -> int:
    # create a string parenthesis depicting the range of numbers allowed to be used in input prints for user
    if start is not None and end is not None:
        parenthesis_of_numbers = f" ({start}-{end})"
    elif start is not None:
        parenthesis_of_numbers = f" ({start}-∞)"
    elif end is not None:
        parenthesis_of_numbers = f" (-∞ - {end})"
    else:
        parenthesis_of_numbers = ""

    user_input = input(f"\nPlease type {string_for_input} as an integer number{parenthesis_of_numbers}: ")
    while True:
        try:
            int(user_input)
            # create the condition required to check if number is in the requested range
            if start is not None and end is not None:
                is_number_in_requested_range = int(user_input) in range(start, end + 1)
            elif start is not None:
                is_number_in_requested_range = int(user_input) >= start
            elif end is not None:
                is_number_in_requested_range = int(user_input) <= end
            else:
                is_number_in_requested_range = True

            if not is_number_in_requested_range:
                print("This is not an acceptable integer.")
                user_input = input(f"Please type {string_for_input} as an integer positive number{parenthesis_of_numbers}: ")
            else:
                return int(user_input)

        except ValueError:
            print("\nThis is is not an integer.")
            user_input = input(f"Please type {string_for_input} as an integer number{parenthesis_of_numbers}: ")


# player x is "X" or "O"
def player_plays(x: str, status_list):
    while True:
        row = check_if_int("the ROW of the cell you want to mark", 1, 3) - 1
        column = check_if_int("the COLUMN of the cell you want to mark", 1, 3) - 1

        if status_list[row][column] == " ":
            status_list[row][column] = x
            return
        else:
            print("\nThe cell you selected has already been chosen...")


def is_there_tic_tac_toe(box_status:list) -> bool:
    # columns
    for row in range(3):
        if box_status[row][0] == box_status[row][1] == box_status[row][2] != " ":
            return True

    # row
    for column in range(3):
        if box_status[0][column] == box_status[1][column] == box_status[2][column] != " ":
            return True

    # diagonal
    if box_status[0][0] == box_status[1][1] == box_status[2][2] != " ":
        return True

    # inverse of diagonal
    if box_status[0][2] == box_status[1][1] == box_status[2][0] != " ":
        return True

    return False


def one_game() -> str:  # it returns "X", "O" or "draw"
    status_list = deepcopy(box_status)
    player = choice(["X", "O"])
    for rnd in range(1, 10):
        print(f"\nRound {rnd}")
        print(f"\nPlayer '{player}' plays.")

        print_box(status_list)

        player_plays(player, status_list)

        if rnd >= 5 and is_there_tic_tac_toe(status_list):
            print_box(status_list)
            print(f"\nPlayer '{player}' wins!!!")
            return player

        if player == "X":
            player = "O"
        else:
            player = "X"
    else:
        print("\nThere is no winner in this round...")
        return "draw"


# main
def main():
    score = {"X": 0, "O": 0, "draw": 0}
    print(f"\nplayer 'X' |{score["X"]} - {score["O"]}| player 'O'"
          f"\ndraws: {score["draw"]}")

    for game in range(1, total_games + 1):
        print(f"\nGame {game}")
        result = one_game()

        if result == "X":
            score["X"] += 1
        elif result == "O":
            score["O"] += 1
        else:
            score["draw"] += 1

        print(f"\nplayer 'X' |{score["X"]} - {score["O"]}| player 'O'"
              f"\ndraws: {score["draw"]}")

    return


main()
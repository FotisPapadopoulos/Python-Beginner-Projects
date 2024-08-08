# rules of YAHTZEE: https://www.hasbro.com/common/instruct/yahtzee.pdf

# this is a program that simulates the game of YAHTZEE
# just run it and the program will ask you how many players (2-10) and how many games (1-10) you want to play
# after that you begin to play
# at the end of every game the program displays the total wins of each player
# at the end of the total games the program will display the winner/winners that got the most wins

from random import randrange
from copy import deepcopy

# globals
active_dices = [1, 2, 3, 4, 5]
score_card = {"Upper Section": {"Ones": None, "Twos": None, "Threes": None,
                                "Fours": None, "Fives": None, "Sixes": None},
              "Lower Section": {"3 of a kind": None, "4 of a kind": None, "Full house": None,
                                "Small straight": None, "Large straight": None, "YAHTZEE": None, "Chance": None},
              "yahtzee_bonus": 0}
yahtzee_bonus = 0


# functions
def yes_or_no() -> str:
    user_choice = input("\nPlease type 'yes' or 'no': ").strip().lower()
    while True:
        if user_choice == "yes" or user_choice == "no":
            return user_choice
        else:
            print("\nThis is not a valid answer.")
            user_choice = input("Please type 'yes' or 'no': ").strip().lower()


def roll_dice(number_of_dices):
    for pos in range(number_of_dices):
        active_dices[pos] = randrange(1, 6 + 1, 1)


def print_active_dice_numbers(active_dices: list):
    print(f"\n1st dice: {active_dices[0]}, 2nd dice: {active_dices[1]}, 3rd dice: {active_dices[2]}, "
          f"4th dice: {active_dices[3]}, 5th dice: {active_dices[4]}")


def check_if_int_and_return_it(start=None, end=None) -> int:
    if not start is None and not end is None:
        user_input = input(f"\nPlease type an integer number between {start} and {end}: ").strip()
        while True:
            try:
                user_input = int(user_input)
                if user_input in range(start, end + 1):
                    return user_input
                else:
                    print("\nThis number is not between the accepted range.")
                    user_input = input(f"Please type an integer number between {start} and {end}: ").strip()
            except ValueError:
                print("\nThis is not an integer number.")
                user_input = input(f"Please type an integer number between {start} and {end}: ").strip()
    elif start is None and end is None:
        user_input = input("\nPlease type an integer number: ").strip()
        while True:
            try:
                return int(user_input)
            except ValueError:
                print("\nThis is not an integer number.")
                user_input = input("Please type an integer number: ").strip()
    elif end is None:
        user_input = input(f"\nPlease type an integer number bigger or equal to {start}: ").strip()
        while True:
            try:
                user_input = int(user_input)
                if user_input >= start:
                    return user_input
                else:
                    print("\nThis number is not between the accepted range.")
                    user_input = input(f"Please type an integer number bigger or equal to {start}: ").strip()
            except ValueError:
                print("\nThis is not a valid answer.")
                user_input = input(f"Please type an integer number bigger or equal to {start}: ").strip()
    else:  # start is None
        user_input = input(f"\nPlease type an integer number smaller or equal to {end}: ").strip()
        while True:
            try:
                user_input = int(user_input)
                if user_input <= end:
                    return user_input
                else:
                    print("\nThis number is not between the accepted range.")
                    user_input = input(f"Please type an integer number smaller or equal to {end}: ").strip()
            except ValueError:
                print("\nThis is not an integer.")
                user_input = input(f"Please type an integer number smaller or equal to {end}: ").strip()


def calculate_upper_section(dice_numbers: list, category: str) -> int:
    s = 0
    if category == "ones":
        for number in dice_numbers:
            if number == 1:
                s += 1
        return s
    elif category == "twos":
        for number in dice_numbers:
            if number == 2:
                s += 2
        return s
    elif category == "threes":
        for number in dice_numbers:
            if number == 3:
                s += 3
        return s
    elif category == "fours":
        for number in dice_numbers:
            if number == 4:
                s += 4
        return s
    elif category == "fives":
        for number in dice_numbers:
            if number == 5:
                s += 5
        return s
    elif category == "sixes":
        for number in dice_numbers:
            if number == 6:
                s += 6
        return s


def upper_section_bonus_value(upper_section: dict) -> int:
    s = 0
    for value in upper_section.values():
        if not value is None:
            s += value
    if s >= 63:
        return 63
    else:
        return 0


def x_of_a_kind_value(x: int, dice_numbers: list) -> int:
    s = sum(dice_numbers)
    myList = []
    for number in range(1, 6 + 1):
        myList.append([number2 for number2 in dice_numbers if number2 == number])

    for l in myList:
        if len(l) >= x:
            return s
    else:
        return 0


def full_house_value(dice_numbers: list) -> int:
    s = set(dice_numbers)
    l = len(s)
    if l == 2:
        number1 = list(s)[0]
        number2 = list(s)[1]
        s2 = {dice_numbers.count(number1), dice_numbers.count(number2)}
        if 2 in s2 and 3 in s2:
            return 25
        else:
            return 0
    else:
        return 0


def small_straight_value(dice_numbers: list) -> int:
    if len(set(dice_numbers)) >= 4:
        sorted_list = sorted(set(dice_numbers))
        if len(sorted_list) == 4:
            for pos in range(0, 3):
                if sorted_list[pos + 1] != sorted_list[pos] + 1:
                    break
            else:
                return 30
        else:  # len(sorted_list) == 5
            for pos in range(0, 4):
                if sorted_list[pos + 1] != sorted_list[pos] + 1:
                    break
            else:
                return 30

        return 0
    else:
        return 0


def large_straight_value(dice_numbers: list) -> int:
    s = set(dice_numbers)
    if len(s) == 5:
        sorted_list = sorted(dice_numbers)
        for pos in range(0, 3):
            if sorted_list[pos + 1] != sorted_list[pos] + 1:
                break
        else:
            return 40
        return 0
    else:
        return 0


def yahtzee_value(dice_numbers: list) -> int:
    x = dice_numbers[0]
    for number in dice_numbers[1:]:
        if not number == x:
            return 0
    else:
        return 50


def chance(dice_numbers: list) -> int:
    s = 0
    for number in dice_numbers:
        s += number
    return s


def upper_section_bonus(upper_section: dict) -> int:
    s = 0
    for value in upper_section.values():
        if value is None:
            continue
        else:
            s += value
    if s >= 63:
        return 35
    else:
        return 0


def total_value_of_scorecard(scorecard: dict) -> int:
    s = upper_section_bonus(scorecard["Upper Section"])
    s += scorecard["yahtzee_bonus"] * 100
    for section_name, section_dict in scorecard.items():
        if section_name != "yahtzee_bonus":
            for cat_value in section_dict.values():
                if not cat_value is None:
                    s += cat_value
    return s


def print_player_scorecard_and_its_possible_values_and_return_list_of_available_categories(scorecard: dict, \
                                                                                           possible_values: dict, \
                                                                                           player: str) \
        -> list:
    print()

    print(f"{player} Possible Scorecard")
    print(f"YAHTZEE BONUS: {scorecard["yahtzee_bonus"]}, total score: {total_value_of_scorecard(scorecard)}")
    mydict = tuple(list(scorecard["Upper Section"].items()) + list(scorecard["Lower Section"].items()))
    dict_possible = tuple(list(possible_values["Upper Section"].items()) + \
                          list(possible_values["Lower Section"].items()))

    print()
    print("|" + "Upper Section".center(14) + "|" + " " * 16 + "|" + "Lower Section".center(14) + "|")

    cnt_of_available_categories = 0
    available_categories_list = []

    # print the upper and lower sections (yahtzee bonus not included)
    for pos in range(6):
        up_key, up_key_possible = mydict[pos][0], dict_possible[pos][0]
        up_value, up_value_possible = mydict[pos][1], dict_possible[pos][1]
        l_key, l_key_possible = mydict[pos + 6][0], dict_possible[pos + 6][0]
        l_value, l_value_possible = mydict[pos + 6][1], dict_possible[pos + 6][1]
        print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")

        if not up_value is None and not l_value is None:
            print("|" + up_key.center(14) + "|" + str(up_value).center(5) + "|" \
                  + " " * 10 + "|" + l_key.center(14) + "|" + str(l_value).center(5) + "|")
        elif up_value is None and not l_value is None:
            cnt_of_available_categories += 1
            available_categories_list.append(up_key)

            print("|" + up_key.center(14) + "|" + f"({str(up_value_possible)})".center(5) + "|" \
                  + f"({cnt_of_available_categories})".center(4) + \
                  " " * 6 + "|" + l_key.center(14) + "|" + str(l_value).center(5) + "|")
        elif up_value is None and l_value is None:
            cnt_of_available_categories += 2
            available_categories_list.append(up_key)
            available_categories_list.append(l_key)

            print("|" + up_key.center(14) + "|" + f"({str(up_value_possible)})".center(5) + "|" \
                  + f"({cnt_of_available_categories - 1})".center(4) \
                  + " " * 6 + "|" + l_key.center(14) + "|" + f"({str(l_value_possible)})".center(5) + "|" \
                  + f"({cnt_of_available_categories})")
        else:  # not up_value is None and l_value is None
            cnt_of_available_categories += 1
            available_categories_list.append(l_key)

            print("|" + up_key.center(14) + "|" + str(up_value).center(5) + "|" \
                  + " " * 10 + "|" + l_key.center(14) + "|" + f"({str(l_value_possible)})".center(5) + "|" + \
                  f"({cnt_of_available_categories})")

    # print the upper bonus and the chance section from the lower section
    print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")

    # upper bonus and chance section print
    if mydict[12][1] is None:
        cnt_of_available_categories += 1
        available_categories_list.append(mydict[12][0])
        print("|" + "Upper Bonus".center(14) + "|" + \
              str(upper_section_bonus(scorecard["Upper Section"])).center(5) + "|" \
              + " " * 10 + "|" + str(mydict[12][0]).center(14) + "|" + f"({dict_possible[12][1]})".center(5) + "|" \
              + f"({cnt_of_available_categories})")
    else:  # chance category is not available
        print("|" + "Upper Bonus".center(14) + "|" + \
              str(upper_section_bonus(scorecard["Upper Section"])).center(5) + "|" \
              + " " * 10 + "|" + str(mydict[12][0]).center(14) + "|" + str(mydict[12][1]).center(5) + "|")

    print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")
    print()
    return available_categories_list


def print_player_scorecard_without_possible_values(scorecard: dict, player: str):
    print()

    print(f"{player} Scorecard")
    print(f"YAHTZEE BONUS: {scorecard["yahtzee_bonus"]}, total score: {total_value_of_scorecard(scorecard)}")
    key_and_value_tuple = tuple(list(scorecard["Upper Section"].items()) + list(scorecard["Lower Section"].items()))
    list_of_values = [t[1] for t in key_and_value_tuple]

    print()
    print("|" + "Upper Section".center(14) + "|" + " " * 16 + "|" + "Lower Section".center(14) + "|")

    # print the upper and lower sections (yahtzee bonus not included)
    for pos in range(6):
        up_key = key_and_value_tuple[pos][0]
        up_value = key_and_value_tuple[pos][1]
        l_key = key_and_value_tuple[pos + 6][0]
        l_value = key_and_value_tuple[pos + 6][1]
        print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")

        if not up_value is None and not l_value is None:
            print("|" + up_key.center(14) + "|" + str(up_value).center(5) + "|" \
                  + " " * 10 + "|" + l_key.center(14) + "|" + str(l_value).center(5) + "|")
        elif up_value is None and not l_value is None:

            print("|" + up_key.center(14) + "|" + "".center(5) + "|" \
                  + " " * 10 + "|" + l_key.center(14) + "|" + str(l_value).center(5) + "|")
        elif up_value is None and l_value is None:

            print("|" + up_key.center(14) + "|" + "".center(5) + "|" \
                  + " " * 10 + "|" + l_key.center(14) + "|" + "".center(5) + "|")
        else:  # not up_value is None and l_value is None

            print("|" + up_key.center(14) + "|" + str(up_value).center(5) + "|" \
                  + " " * 10 + "|" + l_key.center(14) + "|" + "".center(5) + "|")

    # print the upper bonus and the chance section from the lower section
    print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")

    # upper bonus and chance section print
    if None in list_of_values:  # upper bonus should be displayed as 63 or ""
        upper_bonus = upper_section_bonus(scorecard["Upper Section"])
        if upper_bonus == 0:
            upper_bonus = ""
    else:  # upper bonus should be displayed as 63 or 0
        upper_bonus = upper_section_bonus(scorecard["Upper Section"])

    if key_and_value_tuple[12][1] is None:
        print("|" + "Upper Bonus".center(14) + "|" + \
              str(upper_bonus).center(5) + "|" \
              + " " * 10 + "|" + str(key_and_value_tuple[12][0]).center(14) + "|" + "".center(5) + "|")
    else:  # chance category is not available
        print("|" + "Upper Bonus".center(14) + "|" + \
              str(upper_bonus).center(5) + "|" \
              + " " * 10 + "|" + str(key_and_value_tuple[12][0]).center(14) + "|" + str(
            key_and_value_tuple[12][1]).center(5) + "|")

    print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")
    print()


def print_possible_scorecard_for_joker_rules_when_lower_section_is_available(scorecard: dict,\
                                                                             possible_values: dict, player: str) \
    -> list:
    print()

    print(f"{player} Possible Scorecard")
    print(f"YAHTZEE BONUS: {scorecard["yahtzee_bonus"]}, total score: {total_value_of_scorecard(scorecard)}")
    mydict = tuple(list(scorecard["Upper Section"].items()) + list(scorecard["Lower Section"].items()))
    dict_possible = tuple(list(possible_values["Upper Section"].items()) + \
                          list(possible_values["Lower Section"].items()))

    print()
    print("|" + "Upper Section".center(14) + "|" + " " * 16 + "|" + "Lower Section".center(14) + "|")

    cnt_of_available_categories = 0
    available_categories_list = []

    # print the upper and lower sections (yahtzee bonus not included)
    for pos in range(6):
        up_key = mydict[pos][0]
        up_value = mydict[pos][1]
        l_key, l_key_possible = mydict[pos + 6][0], dict_possible[pos + 6][0]
        l_value, l_value_possible = mydict[pos + 6][1], dict_possible[pos + 6][1]
        print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")

        if not up_value is None and not l_value is None:
            print("|" + up_key.center(14) + "|" + str(up_value).center(5) + "|" \
                  + " " * 10 + "|" + l_key.center(14) + "|" + str(l_value).center(5) + "|")
        elif up_value is None and not l_value is None:

            print("|" + up_key.center(14) + "|" + "".center(5) + "|" \
                  + " " * 10 + "|" + l_key.center(14) + "|" + str(l_value).center(5) + "|")
        elif up_value is None and l_value is None:
            cnt_of_available_categories += 1
            available_categories_list.append(l_key)

            print("|" + up_key.center(14) + "|" + "".center(5) + "|" \
                  + " " * 10 + "|" + l_key.center(14) + "|" + f"({str(l_value_possible)})".center(5) + "|" \
                  + f"({cnt_of_available_categories})")
        else:  # not up_value is None and l_value is None
            cnt_of_available_categories += 1
            available_categories_list.append(l_key)

            print("|" + up_key.center(14) + "|" + str(up_value).center(5) + "|" \
                  + " " * 10 + "|" + l_key.center(14) + "|" + f"({str(l_value_possible)})".center(5) + "|" + \
                  f"({cnt_of_available_categories})")

    # print the upper bonus and the chance section from the lower section
    print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")

    # upper bonus and chance section print
    if mydict[12][1] is None:
        cnt_of_available_categories += 1
        available_categories_list.append(mydict[12][0])
        print("|" + "Upper Bonus".center(14) + "|" + \
              str(upper_section_bonus(scorecard["Upper Section"])).center(5) + "|" \
              + " " * 10 + "|" + str(mydict[12][0]).center(14) + "|" + f"({dict_possible[12][1]})".center(5) + "|" \
              + f"({cnt_of_available_categories})")
    else:  # chance category is not available
        print("|" + "Upper Bonus".center(14) + "|" + \
              str(upper_section_bonus(scorecard["Upper Section"])).center(5) + "|" \
              + " " * 10 + "|" + str(mydict[12][0]).center(14) + "|" + str(mydict[12][1]).center(5) + "|")

    print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")
    print()
    return available_categories_list


def print_possible_scorecard_for_joker_rules_when_lower_section_is_NOT_available(scorecard: dict, \
                                                                                 possible_values: dict, player: str):
    print()

    print(f"{player} Possible Scorecard")
    print(f"YAHTZEE BONUS: {scorecard["yahtzee_bonus"]}, total score: {total_value_of_scorecard(scorecard)}")
    mydict = tuple(list(scorecard["Upper Section"].items()) + list(scorecard["Lower Section"].items()))
    dict_possible = tuple(list(possible_values["Upper Section"].items()) + \
                          list(possible_values["Lower Section"].items()))

    print()
    print("|" + "Upper Section".center(14) + "|" + " " * 16 + "|" + "Lower Section".center(14) + "|")

    cnt_of_available_categories = 0
    available_categories_list = []

    # print the upper and lower sections (yahtzee bonus not included)
    for pos in range(6):
        up_key, up_key_possible = mydict[pos][0], dict_possible[pos][0]
        up_value, up_value_possible = mydict[pos][1], dict_possible[pos][1]
        l_key = mydict[pos + 6][0]
        l_value = mydict[pos + 6][1]
        print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")

        if not up_value is None and not l_value is None:
            print("|" + up_key.center(14) + "|" + str(up_value).center(5) + "|" \
                  + " " * 10 + "|" + l_key.center(14) + "|" + str(l_value).center(5) + "|")
        elif up_value is None and not l_value is None:
            cnt_of_available_categories += 1
            available_categories_list.append(up_key)

            print("|" + up_key.center(14) + "|" + f"({str(up_value_possible)})".center(5) + "|" \
                  + f"({cnt_of_available_categories})".center(4) + \
                  " " * 6 + "|" + l_key.center(14) + "|" + str(l_value).center(5) + "|")
        elif up_value is None and l_value is None:
            cnt_of_available_categories += 1
            available_categories_list.append(up_key)

            print("|" + up_key.center(14) + "|" + f"({str(up_value_possible)})".center(5) + "|" \
                  + f"({cnt_of_available_categories - 1})".center(4) \
                  + " " * 6 + "|" + l_key.center(14) + "|" + "".center(5) + "|")
        else:  # not up_value is None and l_value is None

            print("|" + up_key.center(14) + "|" + str(up_value).center(5) + "|" \
                  + " " * 10 + "|" + l_key.center(14) + "|" + "".center(5) + "|")

    # print the upper bonus and the chance section from the lower section
    print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")

    # upper bonus and chance section print
    if mydict[12][1] is None:
        cnt_of_available_categories += 1
        available_categories_list.append(mydict[12][0])
        print("|" + "Upper Bonus".center(14) + "|" + \
              str(upper_section_bonus(scorecard["Upper Section"])).center(5) + "|" \
              + " " * 10 + "|" + str(mydict[12][0]).center(14) + "|" + "".center(5) + "|")
    else:  # chance category is not available
        print("|" + "Upper Bonus".center(14) + "|" + \
              str(upper_section_bonus(scorecard["Upper Section"])).center(5) + "|" \
              + " " * 10 + "|" + str(mydict[12][0]).center(14) + "|" + str(mydict[12][1]).center(5) + "|")

    print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")
    print()
    return available_categories_list


    # print the upper bonus and the chance section from the lower section
    print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")

    # upper bonus and chance section print
    if mydict[12][1] is None:
        cnt_of_available_categories += 1
        available_categories_list.append(mydict[12][0])
        print("|" + "Upper Bonus".center(14) + "|" + \
              str(upper_section_bonus(scorecard["Upper Section"])).center(5) + "|" \
              + " " * 10 + "|" + str(mydict[12][0]).center(14) + "|" + f"({dict_possible[12][1]})".center(5) + "|" \
              + f"({cnt_of_available_categories})")
    else:  # chance category is not available
        print("|" + "Upper Bonus".center(14) + "|" + \
              str(upper_section_bonus(scorecard["Upper Section"])).center(5) + "|" \
              + " " * 10 + "|" + str(mydict[12][0]).center(14) + "|" + str(mydict[12][1]).center(5) + "|")

    print("|" + "-" * 14 + "|" + "-----" + "|" + " " * 10 + "|" + "-" * 14 + "|" + "-----" + "|")
    print()
    return available_categories_list
# it will move keepers to the right side of the active_dices list, and return a list containing the positions of the
# keepers on the active_dices list, if there are no keepers it will return 0
def check_input_for_keepers_and_return_positions_of_keepers(dice_numbers: list):
    print("\nDo you want to set any keepers?")

    if yes_or_no() == "yes":
        user_input = input("\nPlease type the order number of the dices you want to keep, "
                           "using commas (i.e. '2, 4, 5'), \nor if you changed your mind and don't "
                           "want to set any keepers type ',': ").replace(" ", "")

        while True:
            number_of_commas = user_input.count(",")
            user_input_list = user_input.split(",")

            # in case the user changed their mind after they said 'yes' and they don't want to keep any keepers
            if user_input == ",":
                return 0

            if len(user_input_list) <= 4:
                for element in user_input_list:
                    try:
                        element = int(element)
                        if not element in range(1, 5 + 1):
                            print("\nOne of the elements is not an integer number between 1 and 5.")
                            user_input = input("Please type the order number of the dices you want to keep, "
                                               "using commas (i.e. '2, 4, 5'), \nor if you changed your mind and don't "
                                               "want to set any keepers type ',': ").replace(" ", "")
                            break
                    except ValueError:
                        print("\nOne of the elements is not an integer number.")
                        user_input = input("Please type the order number of the dices you want to keep, "
                                           "using commas (i.e. '2, 4, 5'), \nor if you changed your mind and don't "
                                           "want to set any keepers type ',': ").replace(" ", "")
                        break
                else:
                    return [int(x) for x in user_input_list]
            else:
                print("\nYou can only set up to 4 keepers.")
                user_input = input("Please type the order number of the dices you want to keep, "
                                   "using commas (i.e. '2, 4, 5'), \nor if you changed your mind and don't "
                                   "want to set any keepers type ',': ").replace(" ", "")
    else:
        return 0


def dict_containing_the_possible_values_of_the_None_categories(dice_numbers: list, player_scorecard: dict) -> dict:
    possible_values = deepcopy(score_card)
    for section_name, section in player_scorecard.items():
        if section_name != "yahtzee_bonus":
            for category_name, category_value in section.items():
                if category_value is None:
                    if category_name == "Ones":
                        possible_values[section_name][category_name] = \
                            calculate_upper_section(dice_numbers, "ones")
                    elif category_name == "Twos":
                        possible_values[section_name][category_name] = \
                            calculate_upper_section(dice_numbers, "twos")
                    elif category_name == "Threes":
                        possible_values[section_name][category_name] = \
                            calculate_upper_section(dice_numbers, "threes")
                    elif category_name == "Fours":
                        possible_values[section_name][category_name] = \
                            calculate_upper_section(dice_numbers, "fours")
                    elif category_name == "Fives":
                        possible_values[section_name][category_name] = \
                            calculate_upper_section(dice_numbers, "fives")
                    elif category_name == "Sixes":
                        possible_values[section_name][category_name] = \
                            calculate_upper_section(dice_numbers, "sixes")
                    elif category_name == "3 of a kind":
                        possible_values[section_name][category_name] = \
                            x_of_a_kind_value(3, dice_numbers)
                    elif category_name == "4 of a kind":
                        possible_values[section_name][category_name] = \
                            x_of_a_kind_value(4, dice_numbers)
                    elif category_name == "Full house":
                        possible_values[section_name][category_name] = \
                            full_house_value(dice_numbers)
                    elif category_name == "Small straight":
                        possible_values[section_name][category_name] = \
                            small_straight_value(dice_numbers)
                    elif category_name == "Large straight":
                        possible_values[section_name][category_name] = \
                            large_straight_value(dice_numbers)
                    elif category_name == "YAHTZEE":
                        possible_values[section_name][category_name] = \
                            yahtzee_value(dice_numbers)
                    elif category_name == "Chance":
                        possible_values[section_name][category_name] = \
                            chance(dice_numbers)
    return possible_values


def dict_containing_the_possible_values_of_the_lower_section_for_joker_rules(dice_numbers: list, player_scorecard: dict)\
    -> dict: # it will return 0 if there are no possible values on the lower section
    possible_values = deepcopy(score_card)
    there_is_available_cat = False
    for cat_name, cat_value in player_scorecard["Lower Section"].items():
        if cat_value is None:
            there_is_available_cat = True
            if cat_name == "3 of a kind":
                possible_values["Lower Section"][cat_name] = sum(dice_numbers)
            elif cat_name == "4 of a kind":
                possible_values["Lower Section"][cat_name] = sum(dice_numbers)
            elif cat_name == "Full house":
                possible_values["Lower Section"][cat_name] = 25
            elif cat_name == "Small straight":
                possible_values["Lower Section"][cat_name] = 30
            elif cat_name == "Large straight":
                possible_values["Lower Section"][cat_name] = 40
            elif cat_name == "Chance":
                possible_values["Lower Section"][cat_name] = sum(dice_numbers)
    if there_is_available_cat:
        return possible_values
    else:
        return 0
    

def dict_containing_zeros_for_upper_section_available_categories_for_joker_rules(\
        dice_numbers: list, player_scorecard: dict) -> dict:
    possible_values = deepcopy(player_scorecard)
    for cat_name, cat_value in player_scorecard["Upper Section"].items():
        if cat_value is None:
            possible_values["Upper Section"][cat_name] = 0
    return possible_values


def tuple_of_available_categories_in_a_scorecard(player_scorecard: dict):
    l = []
    for section_name, section_dict in player_scorecard.items():
        if section_name != "yahtzee_bonus":
            for category_name, category_value in section_dict.items():
                if category_value is None:
                    l.append(category_name)
    return l


def player_round(player: str, player_scorecard: dict, rnd:int, game: int):
    global active_dices  # I need to declare that it's a global variable because I am going to modify it if there are
    # any keepers

    print(f"\n{player} plays. Round {rnd}  Game {game}")
    roll_dice(5)

    for rnd in range(1, 3 + 1):
        if rnd == 1:
            try_string = "1st Try"
        elif rnd == 2:
            try_string = "2nd Try"
        else: # rnd == 3
            try_string = "3rd Try"

        print(f"\n{try_string}")

        print_active_dice_numbers(active_dices)

        # if it is the 3rd round we only want to print the dices, there is no roll again and no keepers
        if rnd == 3:
            break

        print("\nDo you want to roll again?")
        if yes_or_no() == "no":
            break

        position_of_keepers = check_input_for_keepers_and_return_positions_of_keepers(active_dices)

        # move the keepers on the right side of the active_dices list, if there are any keepers
        if position_of_keepers != 0:
            temp_list = []
            for pos in position_of_keepers:
                x = active_dices[pos - 1]
                temp_list.append(x)
                active_dices[pos - 1] = 0
            for pos in range(4, -1, -1):
                if active_dices[pos] == 0:
                    active_dices.pop(pos)

            active_dices = active_dices + temp_list
            roll_dice(5 - len(position_of_keepers))
        else:
            roll_dice(5)

    # pass the value to the player's scorecard
    if yahtzee_value(active_dices) == 50 and not player_scorecard["Lower Section"]["YAHTZEE"] is None: # time for joker

        if player_scorecard["Lower Section"]["YAHTZEE"] != 0:
            player_scorecard["yahtzee_bonus"] += 1
            print(f"\n{player} gets an extra 100 bonus points because they have already scored a yahtzee in previous"\
                  " rounds")

            joker_rules(player_scorecard, player)

            print_player_scorecard_without_possible_values(player_scorecard, player)
        else:  # JOKER rules, no bonus

            print(f"Unfortunately you have already filled in 'YAHTZEE' section with a zero, and you don't get the 100 "
                  f"point bonus.")

            joker_rules(player_scorecard, player)

            print_player_scorecard_without_possible_values(player_scorecard, player)

    else:  # no second or more yahtzee
        possible_values = dict_containing_the_possible_values_of_the_None_categories(active_dices, player_scorecard)

        list_of_available_categories = \
            print_player_scorecard_and_its_possible_values_and_return_list_of_available_categories( \
                player_scorecard, possible_values, player)

        fill_the_player_scorecard_depending_on_the_user_input_or_automatically_if_there_is_only_one_available_category(\
            player_scorecard, player,possible_values, list_of_available_categories)

        print_player_scorecard_without_possible_values(player_scorecard, player)


def joker_rules(player_scorecard, player):
    upper_section_category_name = \
        list(player_scorecard["Upper Section"].keys())[active_dices[0] - 1]
    upper_section_category_value = \
        list(player_scorecard["Upper Section"].values())[active_dices[0] - 1]

    if upper_section_category_value is None: # upper section category is available
        s = sum(active_dices)
        print(
            f"\n'{upper_section_category_name} is empty, therefore it is automatically filled in with {s}'")
        player_scorecard["Upper Section"][upper_section_category_name] = s
    else:  # upper section category for joker rules is NOT available
        print(f"\n'{upper_section_category_name}' is not available. Therefore you will have to choose one"
              f" lower section category that is available.")
        possible_values = dict_containing_the_possible_values_of_the_lower_section_for_joker_rules(active_dices, \
                                                                                                   player_scorecard)
        if possible_values == 0:  # no available categories at the lower section for joker rules
            print("\nUnfortunately there are no available categories on the lower section. Therefore you will"
                  " have fill in with 0 one upper section available category.")

            possible_values = dict_containing_zeros_for_upper_section_available_categories_for_joker_rules( \
                active_dices, player_scorecard)

            list_of_available_categories = \
                print_possible_scorecard_for_joker_rules_when_lower_section_is_NOT_available( \
                    player_scorecard, possible_values, player)

            fill_the_player_scorecard_depending_on_the_user_input_or_automatically_if_there_is_only_one_available_category( \
                player_scorecard, player, possible_values, list_of_available_categories)

        else:  # there are available categories at the lower section for joker rules
            list_of_available_categories = \
                print_possible_scorecard_for_joker_rules_when_lower_section_is_available( \
                    player_scorecard, possible_values, player)

            fill_the_player_scorecard_depending_on_the_user_input_or_automatically_if_there_is_only_one_available_category( \
                player_scorecard, player, possible_values, list_of_available_categories)


def fill_the_player_scorecard_depending_on_the_user_input_or_automatically_if_there_is_only_one_available_category( \
        player_scorecard: dict, player: str, possible_values: dict, list_of_available_categories: list):

    l = len(list_of_available_categories)
    if l == 1:
        try:
            player_scorecard["Upper Section"][list_of_available_categories[0]] = \
                possible_values["Upper Section"][list_of_available_categories[0]]
        except KeyError:
            player_scorecard["Lower Section"][list_of_available_categories[0]] = \
                possible_values["Lower Section"][list_of_available_categories[0]]

        print(f"'{list_of_available_categories[0]}' was the only available choice on the lower section, therefore"
              f" it was automatically filled in with 0.")
    else:
        print("\nPlease select which available category you want to fill in with 0.")
        user_choice = check_if_int_and_return_it(1, l) - 1
        try:
            player_scorecard["Upper Section"][list_of_available_categories[user_choice]] = \
                possible_values["Upper Section"][list_of_available_categories[user_choice]]
        except KeyError:
            player_scorecard["Lower Section"][list_of_available_categories[user_choice]] = \
                possible_values["Lower Section"][list_of_available_categories[user_choice]]


def main():
    print("\nIt's time to play YAHTZEE!!!")

    print("\nBelow you will type the number of players that will play (2-10).")
    number_of_players = check_if_int_and_return_it(2, 10)

    print("\nBelow you will type the number of games you want to play (1 - 10).")
    number_of_games = check_if_int_and_return_it(start=1, end=10)

    players_total_wins_dict = {} # to be used as a history for the wins of each player

    for game_number in range(1, number_of_games + 1):
        players_scorecards = {}

        for number in range(1, number_of_players + 1):
            players_scorecards[f"Player {number}"] = deepcopy(score_card)
            players_total_wins_dict[f"Player {number}"] = 0

        for rnd in range(1, 14):
            for player_number in range(1, number_of_players + 1):
                player_name = "Player " + str(player_number)
                player_round(player_name, players_scorecards[f"Player {player_number}"],rnd, game_number)

        # print a table showing the player's scorecards
        print(f"\nPlayers' total scores for game {game_number}")
        print("\n|" + "-"*10 + "|" + "-"*8 + "|")
        for player_name, player_scorecard in players_scorecards.items():
            x = total_value_of_scorecard(player_scorecard)
            print("|" + player_name.center(10) + "|" + str(x).center(8) + "|")
            print("|" + "-"*10 + "|" + "-"*8 + "|")

        # check who is the winner on a specific game
        maximum = total_value_of_scorecard(players_scorecards["Player 1"])
        winner_numbers_list = [1]
        for player_number in range(2, number_of_players + 1):
            value = total_value_of_scorecard(players_scorecards[f"Player {player_number}"])
            if value > maximum:
                maximum = value
                winner_numbers_list = [player_number]
            elif value == maximum:
                winner_numbers_list.append(player_number)

        if len(winner_numbers_list) == 1: # one winner on a specific game
            players_total_wins_dict[f"Player {winner_numbers_list[0]}"] += 1
            print(f"\nPlayer {winner_numbers_list[0]} wins this game!!!")

        else:  # multiple winners on a specific game
            print(f"\nIt's a draw!!!")
            if len(winner_numbers_list) < number_of_players:  # not all the players won

                # update total wins of each player
                for number in winner_numbers_list:
                    players_total_wins_dict[f"Player {number}"] += 1

                print(f"\nPlayer {winner_numbers_list[0]}", end="")
                for pos in range(1, len(winner_numbers_list)):
                    print(f" and {winner_numbers_list[pos]}", end="")
                print(f" win this game!!!")

            else: # all the players won
                for key in players_total_wins_dict.keys():
                    players_total_wins_dict[key] += 1
                print("\nAll of the players win this game!!!")

        # print table of players' wins
        print("\n|" + "-" * 10 + "|" + "wins".center(8) + "|")
        print("|" + "-" * 10 + "|" + "-" * 8 + "|")
        for player_name, wins in players_total_wins_dict.items():
            x = wins
            print("|" + player_name.center(10) + "|" + str(x).center(8) + "|")
            print("|" + "-" * 10 + "|" + "-" * 8 + "|")

    maximum_wins = max(list(players_total_wins_dict.values()))
    final_winner_names_after_the_end_of_games = []
    for key in players_total_wins_dict.keys():
        if players_total_wins_dict[key] == maximum_wins:
            final_winner_names_after_the_end_of_games.append(key)

    l = len(final_winner_names_after_the_end_of_games)
    if l == 1:
        print(f"\n{final_winner_names_after_the_end_of_games[0]} wins the 'best of {number_of_games}' series.")
    else:  # multiple winners
        print(f"\n{final_winner_names_after_the_end_of_games[0]}", end="")
        for pos in range(1, l):
            if pos < l - 1:
                print(f", {final_winner_names_after_the_end_of_games[pos]}", end="")
            else:  # pos = l - 1
                print(f" and {final_winner_names_after_the_end_of_games[pos]}", end="")
        print(f" win the 'best of {number_of_games}' series.")


main()



# players_total_wins_dict = {"Player 1": 2, "Player 2": 2, "Player 3": 2}
# number_of_games = 10
#
# maximum_wins = max(list(players_total_wins_dict.values()))
# final_winner_names_after_the_end_of_games = []
# for key in players_total_wins_dict.keys():
#     if players_total_wins_dict[key] == maximum_wins:
#         final_winner_names_after_the_end_of_games.append(key)
#
# l = len(final_winner_names_after_the_end_of_games)
# if l == 1:
#     print(f"\n{final_winner_names_after_the_end_of_games[0]} wins the 'best of {number_of_games}' series.")
# else:  # multiple winners
#     print(f"\n{final_winner_names_after_the_end_of_games[0]}", end="")
#     for pos in range(1, l):
#         if pos < l - 1:
#             print(f", {final_winner_names_after_the_end_of_games[pos]}", end="")
#         else:  # pos = l - 1
#             print(f" and {final_winner_names_after_the_end_of_games[pos]}", end="")
#     print(f" win the 'best of {number_of_games}' series.")

# score_card1 = {"Upper Section": {"Ones": 200, "Twos": 100, "Threes": 100,
#                                  "Fours": 100, "Fives": 100, "Sixes": 100},
#                "Lower Section": {"3 of a kind": 100, "4 of a kind": 100, "Full house": 100,
#                                  "Small straight": 100, "Large straight": 100, "YAHTZEE": 100, "Chance": 100},
#                "yahtzee_bonus": 0}
# score_card2 = {"Upper Section": {"Ones": 200, "Twos": 100, "Threes": 100,
#                                  "Fours": 100, "Fives": 100, "Sixes": 100},
#                "Lower Section": {"3 of a kind": 100, "4 of a kind": 100, "Full house": 100,
#                                  "Small straight": 100, "Large straight": 100, "YAHTZEE": 100, "Chance": 100},
#                "yahtzee_bonus": 0}
# score_card3 = {"Upper Section": {"Ones": 200, "Twos": 100, "Threes": 100,
#                                  "Fours": 100, "Fives": 100, "Sixes": 100},
#                "Lower Section": {"3 of a kind": 100, "4 of a kind": 100, "Full house": 100,
#                                  "Small straight": 100, "Large straight": 100, "YAHTZEE": 100, "Chance": 100},
#                "yahtzee_bonus": 0}
#
# players_scorecards = {"Player 1": score_card1, "Player 2": score_card2, "Player 3": score_card3}
# number_of_players = 3
# players_total_wins_dict = {"Player 1": 0, "Player 2": 0, "Player 3": 0}
#
# # print a table showing the player's scorecards
# print("\n|" + "-" * 10 + "|" + "-" * 8 + "|")
# for player_name, player_scorecard in players_scorecards.items():
#     x = total_value_of_scorecard(player_scorecard)
#     print("|" + player_name.center(10) + "|" + str(x).center(8) + "|")
#     print("|" + "-" * 10 + "|" + "-" * 8 + "|")
#
# # check who is the winner on a specific game
# maximum = total_value_of_scorecard(players_scorecards["Player 1"])
# winner_numbers_list = [1]
# for player_number in range(2, number_of_players + 1):
#     value = total_value_of_scorecard(players_scorecards[f"Player {player_number}"])
#     if value > maximum:
#         maximum = value
#         winner_numbers_list = [player_number]
#     elif value == maximum:
#         winner_numbers_list.append(player_number)
#
# if len(winner_numbers_list) == 1:  # one winner on a specific game
#     players_total_wins_dict[f"Player {winner_numbers_list[0]}"] += 1
#     print(f"\nPlayer {winner_numbers_list[0]} wins this game!!!")
#
# else:  # multiple winners on a specific game
#     print(f"\nIt's a draw!!!")
#     if len(winner_numbers_list) < number_of_players:  # not all the players won
#
#         # update total wins of each player
#         for number in winner_numbers_list:
#             players_total_wins_dict[f"Player {number}"] += 1
#
#         print(f"\nPlayer {winner_numbers_list[0]}", end="")
#         for pos in range(1, len(winner_numbers_list)):
#             print(f" and {winner_numbers_list[pos]}", end="")
#         print(f" win this game!!!")
#
#     else:  # all the players won
#         for key in players_total_wins_dict.keys():
#             players_total_wins_dict[key] += 1
#         print("\nAll of the players win this game!!!")
#
# # print table of players' wins
# print("\n|" + "-" * 10 + "|" + "wins".center(8) + "|")
# print("|" + "-" * 10 + "|" + "-" * 8 + "|")
# for player_name, wins in players_total_wins_dict.items():
#     x = wins
#     print("|" + player_name.center(10) + "|" + str(x).center(8) + "|")
#     print("|" + "-" * 10 + "|" + "-" * 8 + "|")


# only one winner
# multiple winners
    # not all of them
    # all of them


# active_dices = [2, 2, 2, 2, 2]
# score_card = {"Upper Section": {"Ones": 100, "Twos": 200, "Threes": 300,
#                                 "Fours": 400, "Fives": 500, "Sixes": 600},
#               "Lower Section": {"3 of a kind": None, "4 of a kind": None, "Full house": None,
#                                 "Small straight": None, "Large straight": None, "YAHTZEE": None, "Chance": None},
#               "yahtzee_bonus": 0}
# yahtzee_bonus = 0
# score_card2 = {"Upper Section": {"Ones": 100, "Twos": None, "Threes": 100,
#                                  "Fours": 100, "Fives": None, "Sixes": 100},
#                "Lower Section": {"3 of a kind": 100, "4 of a kind": 1, "Full house": 1,
#                                  "Small straight": 1, "Large straight": 1, "YAHTZEE": 50, "Chance": 1},
#                "yahtzee_bonus": 0}
#
# # for number in range(1, 7):
# #     if number == 1:
# #         up_cat = "Ones"
# #     elif number == 2:
# #         up_cat = "Twos"
# #     elif number == 3:
# #         up_cat = "Threes"
# #     elif number == 4:
# #         up_cat = "Fours"
# #     elif number == 5:
# #         up_cat = "Fives"
# #     else:
# #         up_cat = "Sixes"
#
# active_dices = [1, 1, 1, 1, 1]
# print(active_dices)
# # score_card2["Upper Section"][up_cat] = None
#
# joker_rules(score_card2, "Fotis")
# print_player_scorecard_without_possible_values(score_card2, "Fotis")

# yahtzee second time checkkkkk
    # yahtzee is NOT zero (yahtzee bonus should be updated) checkkkkk
        # upper section category is available checkkkkk
        # upper section category is not available checkkkkk
            # only one lower section category checkkkkk
            # multiple lower sections available checkkkk
            # no lower section available (fill with zeros any of the available upper sections available) checkkkkk
                # only one upper section available checkkkkk
                # multiple upper section available categories checkkkkk
    # yahtzee is zero
        # upper section category is available
        # lower section category is available

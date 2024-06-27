# https://www.blackjackclassroom.com/blackjack-basic-strategy-charts#basic-strategy <- basic blackjack strategy chart Source

# the following program simulates how a player plays blackjack by applying the basic blackjack strategy
# there are some initial variables that define the details of the rules
# we intend to see if the player has a significant profit or loss after a long period of time playing blackjack
# by applying the basic blackjack strategy

from random import choice
from copy import deepcopy
from math import ceil, sqrt

# GAME RULES:
# you can split a pair of aces only once in the same round,
# when you split aces you only get one card after the split in each hand,
# dealer stands on 17 or above

# globals
deck = 8 * [(number, color) for number in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "jack", "queen", "king")
            for color in ("heart", "spade", "club", "diamond")]  # how many decks are used

initial_bet_amount_per_round = 10  # the initial bet you make every day you go to the casino
how_many_splits_per_round_allowed = 3  # how many times you can split cards in one round
initial_amount_per_day = 100  # the initial money you start with every day you go to the casino
total_days = 100  # how many days you will go to the casino
max_rounds_per_day = 200  # how many rounds you are allowed to play before leaving the casino


# functions
def table(data: list, columnTitles: list, rowTitles: list):
    # check if data list has any extra tuples, lists, dicts etc in any of its items
    DataIsMultidimensional = False
    for i in data:
        if not (type(i) is int or
            type(i) is str or
            type(i) is float or
            type(i) is bool):
            DataIsMultidimensional = True
            break

    if not DataIsMultidimensional:
        x = max([len(str(data[i])) for i in range(len(data))])
        y = max([len(str(columnTitles[i])) for i in range(len(columnTitles))])
        maxCharVertically = max([x, y])
        maxCharVerticallyForTitles = max([len(rowTitles[i]) for i in range(len(rowTitles))])

        print("\t".expandtabs(maxCharVerticallyForTitles) + "|", end="")
        for j in columnTitles:
            print(f"{str(j).center(maxCharVertically)}|", end="")
        print()
        lenColumnTitles = len(columnTitles)
        print("-" * ((maxCharVertically + 1) * lenColumnTitles + maxCharVerticallyForTitles + 1))

        for i in range(len(rowTitles)):
            print(f"{str(rowTitles[i]).center(maxCharVerticallyForTitles)}|", end="")
            for j in range(lenColumnTitles):
                print(f"{str(data[i * lenColumnTitles + j]).center(maxCharVertically)}|", end="")
            print()
            print("-" * ((maxCharVertically + 1) * lenColumnTitles + maxCharVerticallyForTitles + 1))


def give_random_card(my_deck: list) -> tuple:
    x = choice(list(my_deck))
    my_deck.remove(x)
    return x


def add_value_to_existing_hand(card: tuple, hand: tuple) -> tuple:
    x = card[0]
    my_sum = list(hand)
    if type(x) is int:
        if x != 1:
            my_sum[0] += x
            my_sum[1] += x
        else:
            my_sum[0] += 1
            if my_sum[1] + 11 <= 21:
                my_sum[1] += 11
            else:
                my_sum[1] += 1
    else:
        my_sum[0] += 10
        my_sum[1] += 10

    return tuple(my_sum)


def hand_value(cards_set: list) -> tuple:
    my_sum = [0, 0]
    for my_tuple in cards_set:
        if type(my_tuple[0]) is int:
            if my_tuple[0] != 1:
                my_sum[0] += my_tuple[0]
                my_sum[1] += my_tuple[0]
            else:
                my_sum[0] += 1
                if my_sum[1] + 11 <= 21:
                    my_sum[1] += 11
                else:
                    my_sum[1] = my_sum[0]
        else:
            my_sum[0] += 10
            my_sum[1] += 10

    return tuple(my_sum)


def get_input_and_check_it() -> str:
    x = input("\nType 'hit me' or 'stand': ").strip().lower()
    while True:
        if x != "hit me" and x != "stand":
            print("\nThis is not a valid choice")
            x = input("Type 'hit me' or 'stand': ").strip().lower()
        else:
            return x


def print_cards_and_value(cards_value: tuple, cards: list, who_plays: str):  # who_plays == PC or player
    if who_plays == "PC":
        my_string = "PC"
    elif who_plays == "player":
        my_string = "Your"
    print(f"\n{my_string} cards are: ")
    if cards_value[0] == cards_value[1] or max(cards_value) > 21:
        for card in cards:
            print(f"{card}, ", end="")
        print(f"   value is {cards_value[0]}")
    else:
        if max(cards_value) != 21:
            for card in cards:
                print(f"{card}, ", end="")
            print(f"   value is {cards_value[0]} / {cards_value[1]}")
        else:
            for card in cards:
                print(f"{card}, ", end="")
            print(f"   value is {cards_value[1]}")


def split_logic(cards: list, my_deck: list,
                pc_first_card: tuple,
                split_counter_per_round: int, money_in_pocket):  # returns list of tuples i.e. [('double', 19), ('stand', 17)]
    player_hand = cards
    # print(len(my_deck))
    list_of_first_2_card_values = [player_hand[0][0], player_hand[1][0]]
    hand_value_tuple = hand_value(player_hand)
    # print_cards_and_value(hand_value_tuple, player_hand, "player")
    if 21 in hand_value_tuple:
        # print("\nYou have Blackjack!!!")
        return [("stand", "Blackjack")]

    if 1 in list_of_first_2_card_values:
        if (
                8 in list_of_first_2_card_values or 9 in list_of_first_2_card_values or 10 in list_of_first_2_card_values) or \
                (7 in list_of_first_2_card_values and pc_first_card[0] in [2, 7, 8]):
            x = max(hand_value_tuple)
            return [("stand", x if x <= 21 else min(hand_value_tuple))]
        elif ((7 in list_of_first_2_card_values) and pc_first_card[0] in [3, 4, 5, 6]) or \
                ((6 in list_of_first_2_card_values) and pc_first_card[0] in [3, 4, 5, 6]) or \
                ((5 in list_of_first_2_card_values) and pc_first_card[0] in [4, 5, 6]) or \
                ((4 in list_of_first_2_card_values) and pc_first_card[0] in [4, 5, 6]) or \
                ((3 in list_of_first_2_card_values) and pc_first_card[0] in [5, 6]) or \
                ((2 in list_of_first_2_card_values) and pc_first_card[0] in [5, 6]):
            x = give_random_card(my_deck)
            # print(len(my_deck))
            player_hand.append(x)
            hand_value_tuple = add_value_to_existing_hand(x, hand_value_tuple)
            # print_cards_and_value(hand_value_tuple, player_hand, "player")
            x = max(hand_value_tuple)
            if money_in_pocket >= 2 * initial_bet_amount_per_round:
                return [("double", x if x <= 21 else min(hand_value_tuple))]
            else:
                return [("stand", x if x <= 21 else min(hand_value_tuple))]
            pass  # double down
        elif not list_of_first_2_card_values == [1, 1]:
            x = give_random_card(my_deck)
            # print(len(my_deck))
            player_hand.append(x)
            hand_value_tuple = add_value_to_existing_hand(x, hand_value_tuple)
            # print_cards_and_value(hand_value_tuple, player_hand, "player")

    if split_counter_per_round < how_many_splits_per_round_allowed and list_of_first_2_card_values[0] == \
            list_of_first_2_card_values[1]:
        if list_of_first_2_card_values[0] == 1:
            return [("stand", 12)]
        elif ((list_of_first_2_card_values[0] == 8) or \
                (list_of_first_2_card_values[0] == 1 and pc_first_card[0] in [2, 3, 4, 5, 6, 8, 9]) or \
                (list_of_first_2_card_values[0] == 9 and pc_first_card[0] in [2, 3, 4, 5, 6, 8, 9]) or \
                (list_of_first_2_card_values[0] == 7 and pc_first_card[0] in range(2, 7 + 1)) or \
                (list_of_first_2_card_values[0] == 6 and pc_first_card[0] in range(2, 6 + 1)) or \
                (list_of_first_2_card_values[0] == 4 and pc_first_card[0] in range(5, 6 + 1)) or \
                ((list_of_first_2_card_values[0] == 3 or list_of_first_2_card_values[0] == 2) and pc_first_card[
                    0] in range(2,
                                7 + 1))) and money_in_pocket >= 2 * initial_bet_amount_per_round:
            temp_list = []
            for pos in range(len(player_hand)):
                temp_list.extend(split_logic([player_hand[pos], give_random_card(my_deck)], my_deck, pc_first_card,
                                             split_counter_per_round + 1, money_in_pocket - initial_bet_amount_per_round))
            return temp_list
            pass  # split
        elif list_of_first_2_card_values[0] in [10, "jack", "queen", "king"]:
            return [("stand", 20)]
        elif 9 in list_of_first_2_card_values and pc_first_card[0] in [7, 10, 1, "jack", "queen", "king"]:
            return [("stand", 18)]
        elif 5 in list_of_first_2_card_values and pc_first_card[0] in range(2, 9 + 1):
            x = give_random_card(my_deck)
            # print(len(my_deck))
            player_hand.append(x)
            hand_value_tuple = add_value_to_existing_hand(x, hand_value_tuple)
            # print_cards_and_value(hand_value_tuple, player_hand, "player")
            x = max(hand_value_tuple)
            if money_in_pocket >= 2 * initial_bet_amount_per_round:
                return [("double", x if x <= 21 else min(hand_value_tuple))]
            else:
                return [("stand", x if x <= 21 else min(hand_value_tuple))]
            pass  # double down

    if ((11 in hand_value_tuple) and (pc_first_card[0] in range(2, 10 + 1) or
                                        pc_first_card[0] in [("jack", "queen", "king")])) or \
            ((10 in hand_value_tuple) and (pc_first_card[0] in range(2, 9 + 1))) or \
            ((9 in hand_value_tuple) and pc_first_card[0] in range(3, 6 + 1)):
        x = give_random_card(my_deck)
        # print(len(my_deck))
        player_hand.append(x)
        hand_value_tuple = add_value_to_existing_hand(x, hand_value_tuple)
        # print_cards_and_value(hand_value_tuple, player_hand, "player")
        x = max(hand_value_tuple)
        if money_in_pocket >= 2 * initial_bet_amount_per_round:
            return [("double", x if x <= 21 else min(hand_value_tuple))]
        else:
            return [("stand", x if x <= 21 else min(hand_value_tuple))]
        pass  # double down

    while True:
        if (17 in hand_value_tuple or 18 in hand_value_tuple or 19 in hand_value_tuple) or \
                (20 in hand_value_tuple or 21 in hand_value_tuple) or \
                ((13 in hand_value_tuple or 14 in hand_value_tuple or 15 in hand_value_tuple or \
                  16 in hand_value_tuple) and pc_first_card[0] in range(2, 6 + 1)) or \
                ((12 in hand_value_tuple) and pc_first_card[0] in range(4, 6 + 1)):
            x = max(hand_value_tuple)
            return [("stand", x if x <= 21 else min(hand_value_tuple))]
        else:
            x = give_random_card(my_deck)
            # print(len(my_deck))
            player_hand.append(x)
            hand_value_tuple = add_value_to_existing_hand(x, hand_value_tuple)
            # print_cards_and_value(hand_value_tuple, player_hand, "player")

            if min(hand_value_tuple) > 21:
                return [("burned", min(hand_value_tuple))]
            elif 21 in hand_value_tuple:
                return [("stand", 21)]


def player(player_hand: list, my_deck: list,
           pc_first_card: tuple, money_in_pocket):  # 'burned', 'stand', 'split', 'double' + int or 'Blackjack'
    # print(len(my_deck))
    list_of_first_2_card_values = [player_hand[0][0], player_hand[1][0]]
    hand_value_tuple = hand_value(player_hand)
    # print_cards_and_value(hand_value_tuple, player_hand, "player")
    if 21 in hand_value_tuple:
        # print("\nYou have Blackjack!!!")
        return "stand", "Blackjack"

    if 1 in list_of_first_2_card_values:
        if (
                8 in list_of_first_2_card_values or 9 in list_of_first_2_card_values or 10 in list_of_first_2_card_values) or \
                (7 in list_of_first_2_card_values and pc_first_card[0] in [2, 7, 8]):
            x = max(hand_value_tuple)
            return "stand", x if x <= 21 else min(hand_value_tuple)
        elif ((7 in list_of_first_2_card_values) and pc_first_card[0] in [3, 4, 5, 6]) or \
                ((6 in list_of_first_2_card_values) and pc_first_card[0] in [3, 4, 5, 6]) or \
                ((5 in list_of_first_2_card_values) and pc_first_card[0] in [4, 5, 6]) or \
                ((4 in list_of_first_2_card_values) and pc_first_card[0] in [4, 5, 6]) or \
                ((3 in list_of_first_2_card_values) and pc_first_card[0] in [5, 6]) or \
                ((2 in list_of_first_2_card_values) and pc_first_card[0] in [5, 6]):
            x = give_random_card(my_deck)
            # print(len(my_deck))
            player_hand.append(x)
            hand_value_tuple = add_value_to_existing_hand(x, hand_value_tuple)
            # print_cards_and_value(hand_value_tuple, player_hand, "player")
            x = max(hand_value_tuple)
            if money_in_pocket >= 2 * initial_bet_amount_per_round:
                return "double", x if x <= 21 else min(hand_value_tuple)
            else:
                return "stand", x if x <= 21 else min(hand_value_tuple)
            pass  # double down
        elif not list_of_first_2_card_values == [1, 1]:
            x = give_random_card(my_deck)
            # print(len(my_deck))
            player_hand.append(x)
            hand_value_tuple = add_value_to_existing_hand(x, hand_value_tuple)
            # print_cards_and_value(hand_value_tuple, player_hand, "player")

            if min(hand_value_tuple) > 21:
                return "burned", min(hand_value_tuple)
            # it is the hit option in case we have one ace at least in the


    if list_of_first_2_card_values[0] == list_of_first_2_card_values[1]:
        if ((list_of_first_2_card_values[0] == 1 or list_of_first_2_card_values[0] == 8) or \
                (list_of_first_2_card_values[0] == 1 and pc_first_card[0] in [2, 3, 4, 5, 6, 8, 9]) or \
                (list_of_first_2_card_values[0] == 9 and pc_first_card[0] in [2, 3, 4, 5, 6, 8, 9]) or \
                (list_of_first_2_card_values[0] == 7 and pc_first_card[0] in range(2, 7 + 1)) or \
                (list_of_first_2_card_values[0] == 6 and pc_first_card[0] in range(2, 6 + 1)) or \
                (list_of_first_2_card_values[0] == 4 and pc_first_card[0] in range(5, 6 + 1)) or \
                ((list_of_first_2_card_values[0] == 3 or list_of_first_2_card_values[0] == 2) and
                 pc_first_card[0] in range(2, 7 + 1))) and money_in_pocket >= 2 * initial_bet_amount_per_round:
            temp_list = []
            for pos in range(0, 1 + 1):
                temp_list.extend(split_logic([player_hand[pos], give_random_card(my_deck)], my_deck, pc_first_card, 1,
                                             money_in_pocket - initial_bet_amount_per_round))
            return "split", temp_list
            pass  # split
        elif list_of_first_2_card_values[0] in [10, "jack", "queen", "king"]:
            return "stand", 20
        elif 9 in list_of_first_2_card_values and pc_first_card[0] in [7, 10, 1, "jack", "queen", "king"]:
            return "stand", 18
        elif 5 in list_of_first_2_card_values and pc_first_card[0] in range(2, 9 + 1):
            x = give_random_card(my_deck)
            # print(len(my_deck))
            player_hand.append(x)
            hand_value_tuple = add_value_to_existing_hand(x, hand_value_tuple)
            # print_cards_and_value(hand_value_tuple, player_hand, "player")
            x = max(hand_value_tuple)
            if money_in_pocket >= 2 * initial_bet_amount_per_round:
                return "double", x if x <= 21 else min(hand_value_tuple)
            else:
                return "stand", x if x <= 21 else min(hand_value_tuple)
            pass  # double down

    if ((((11 in hand_value_tuple) and (pc_first_card[0] in range(2, 10 + 1) or
                                            pc_first_card[0] in ["jack", "queen", "king"])) or \
                ((10 in hand_value_tuple) and (pc_first_card[0] in range(2, 9 + 1))) or \
                ((9 in hand_value_tuple) and pc_first_card[0] in range(3, 6 + 1))) and
            len(player_hand) == 2): # len is checked because a card could be added in the check of ace above in the last elif option
            x = give_random_card(my_deck)
            # print(len(my_deck))
            player_hand.append(x)
            hand_value_tuple = add_value_to_existing_hand(x, hand_value_tuple)
            # print_cards_and_value(hand_value_tuple, player_hand, "player")
            x = max(hand_value_tuple)
            if money_in_pocket >= 2 * initial_bet_amount_per_round:
                return "double", x if x <= 21 else min(hand_value_tuple)
            else:
                return "stand", x if x <= 21 else min(hand_value_tuple)
            pass  # double down

    while True:
        if (17 in hand_value_tuple or 18 in hand_value_tuple or 19 in hand_value_tuple) or \
                (20 in hand_value_tuple or 21 in hand_value_tuple) or \
                ((13 in hand_value_tuple or 14 in hand_value_tuple or 15 in hand_value_tuple or \
                  16 in hand_value_tuple) and pc_first_card[0] in range(2, 6 + 1)) or \
                ((12 in hand_value_tuple) and pc_first_card[0] in range(4, 6 + 1)):
            x = max(hand_value_tuple)
            if len(player_hand) > 2:
                return "hit", x if x <= 21 else min(hand_value_tuple)
            else:
                return "stand", x if x <= 21 else min(hand_value_tuple)
        else:
            x = give_random_card(my_deck)
            # print(len(my_deck))
            player_hand.append(x)
            hand_value_tuple = add_value_to_existing_hand(x, hand_value_tuple)
            # print_cards_and_value(hand_value_tuple, player_hand, "player")

            if min(hand_value_tuple) > 21:
                return "burned", min(hand_value_tuple)


def computer(computer_hand: list, my_deck: list,
             value_to_beat: int):  # returns int or "Blackjack" if PC has value 21 with two cards only
    computer_value = hand_value(computer_hand)
    # print_cards_and_value(computer_value, computer_hand, "PC")
    if 21 in computer_value:
        return "Blackjack"

    while True:
        if computer_value[1] <= 21:
            if computer_value[1] in range(17, 21 + 1):
                return computer_value[1]
            else:
                x = give_random_card(my_deck)
                # print(len(my_deck))
                computer_hand.append(x)
                computer_value = add_value_to_existing_hand(x, computer_value)
                # print_cards_and_value(computer_value, computer_hand, "PC")
        elif computer_value[0] <= 21:
            if computer_value[0] in range(17, 21 + 1):
                return computer_value[0]
            else:
                x = give_random_card(my_deck)
                # print(len(my_deck))
                computer_hand.append(x)
                computer_value = add_value_to_existing_hand(x, computer_value)
                # print_cards_and_value(computer_value, computer_hand, "PC")
        else:
            return min(computer_value)


def check_winner(command: str, pc_wins_per_day: int, amount: int, player_wins_per_day: int,
                 final_player_value, computer_hand: list,
                 temp_deck: list) -> tuple:  # returns amount, player_wins_per_day, pc_wins_per_day
    if command == "burned":
        pc_wins_per_day += 1
        amount -= initial_bet_amount_per_round
        return amount, player_wins_per_day, pc_wins_per_day
    elif command == "stand" or command == "hit":
        if final_player_value != "Blackjack" and final_player_value > 21:
            pc_wins_per_day += 1
            amount -= initial_bet_amount_per_round
            return amount, player_wins_per_day, pc_wins_per_day
            # print("\nYou lost unfortunately, your cards value is over 21...")
        else:
            final_computer_value = computer(computer_hand, temp_deck, final_player_value)
            # print(f"{len(temp_deck)}")

            if final_player_value == "Blackjack":
                if final_computer_value != "Blackjack":
                    player_wins_per_day += 1
                    amount += initial_bet_amount_per_round
                    return amount, player_wins_per_day, pc_wins_per_day
                    # print("\nYou win!!!! You have Blackjack and dealer doesn't!!!")
                else:
                    pass
            # print("\nUnbelievable...PC has also Blackjack...It's a draw...")
            elif final_computer_value == "Blackjack":
                if final_player_value != "Blackjack":
                    pc_wins_per_day += 1
                    amount -= initial_bet_amount_per_round
                    return amount, player_wins_per_day, pc_wins_per_day
                    # print("\nAh you lost... PC has blackjack and you don't...")
            else:
                if final_player_value <= 21 and final_computer_value <= 21:
                    if final_player_value > final_computer_value:
                        player_wins_per_day += 1
                        amount += initial_bet_amount_per_round
                        return amount, player_wins_per_day, pc_wins_per_day
                        # print("\nYou win!!!")
                    elif final_player_value < final_computer_value:
                        pc_wins_per_day += 1
                        amount -= initial_bet_amount_per_round
                        return amount, player_wins_per_day, pc_wins_per_day
                        # print("\nAhh you lost...")
                    else:
                        pass
                # print("\nIt's a draw...")
                elif final_player_value <= 21:
                    player_wins_per_day += 1
                    amount += initial_bet_amount_per_round
                    return amount, player_wins_per_day, pc_wins_per_day
                    # print("\nYou win!!!")
                elif final_computer_value <= 21:
                    pc_wins_per_day += 1
                    amount -= initial_bet_amount_per_round
                    return amount, player_wins_per_day, pc_wins_per_day
                    # print("\nAhh you lost...")
    elif command == "double":
        if final_player_value != "Blackjack" and final_player_value > 21:
            pc_wins_per_day += 1
            amount -= 2 * initial_bet_amount_per_round
            return amount, player_wins_per_day, pc_wins_per_day
            # print("\nYou lost unfortunately, your cards value is over 21...")
        else:
            final_computer_value = computer(computer_hand, temp_deck, final_player_value)
            # print(f"{len(temp_deck)}")

            if final_player_value == "Blackjack":
                if final_computer_value != "Blackjack":
                    player_wins_per_day += 1
                    amount += 2 * initial_bet_amount_per_round
                    return amount, player_wins_per_day, pc_wins_per_day
                    # print("\nYou win!!!! You have Blackjack and dealer doesn't!!!")
                else:
                    pass
            # print("\nUnbelievable...PC has also Blackjack...It's a draw...")
            elif final_computer_value == "Blackjack":
                if final_player_value != "Blackjack":
                    pc_wins_per_day += 1
                    amount -= 2 * initial_bet_amount_per_round
                    return amount, player_wins_per_day, pc_wins_per_day
                    # print("\nAh you lost... PC has blackjack and you don't...")
            else:
                if final_player_value <= 21 and final_computer_value <= 21:
                    if final_player_value > final_computer_value:
                        player_wins_per_day += 1
                        amount += 2 * initial_bet_amount_per_round
                        return amount, player_wins_per_day, pc_wins_per_day
                        # print("\nYou win!!!")
                    elif final_player_value < final_computer_value:
                        pc_wins_per_day += 1
                        amount -= 2 * initial_bet_amount_per_round
                        return amount, player_wins_per_day, pc_wins_per_day
                        # print("\nAhh you lost...")
                    else:
                        pass
                # print("\nIt's a draw...")
                elif final_player_value <= 21:
                    player_wins_per_day += 1
                    amount += 2 * initial_bet_amount_per_round
                    return amount, player_wins_per_day, pc_wins_per_day
                    # print("\nYou win!!!")
                elif final_computer_value <= 21:
                    pc_wins_per_day += 1
                    amount -= 2 * initial_bet_amount_per_round
                    return amount, player_wins_per_day, pc_wins_per_day
                    # print("\nAhh you lost...")
    return amount, player_wins_per_day, pc_wins_per_day


# main
def playBlackjack(): # returns history dict which has days as dict containing the rounds as dict containing the basic variables and an int
    history = {}
    playerTotalWins = 0
    pcTotalWins = 0
    dayCnt = 0
    totalMoneyInPocket = 0
    while True: # loop of one day
        dayCnt += 1
        history["Day " + str(dayCnt)] = {}

        player_wins_per_day = 0
        pc_wins_per_day = 0
        rnd_per_day = 0
        MoneyInPocketPerDay = initial_amount_per_day
        while True: # loop of one round
            rnd_per_day += 1
            history["Day " + str(dayCnt)]["Round " + str(rnd_per_day)] = {}

            # print(f"Round: {rnd_per_day}")
            temp_deck = deepcopy(deck)
            computer_hand = [give_random_card(temp_deck), give_random_card(temp_deck)]
            # print(f"\nPC has {computer_hand[0]} (____________)")
            player_hand = [give_random_card(temp_deck), give_random_card(temp_deck)]

            command, final_player_value = player(player_hand, temp_deck, computer_hand[0], MoneyInPocketPerDay)

            if command in ["burned", "stand", "double", "hit"]:
                MoneyInPocketPerDay, player_wins_per_day, pc_wins_per_day = \
                    check_winner(command, pc_wins_per_day, MoneyInPocketPerDay, player_wins_per_day, final_player_value,
                                 computer_hand, temp_deck)


            elif command == "split":
                for my_tuple in final_player_value:
                    command_split = my_tuple[0]
                    final_player_value_split = my_tuple[1]
                    MoneyInPocketPerDay, player_wins_per_day, pc_wins_per_day = \
                        check_winner(command_split, pc_wins_per_day, MoneyInPocketPerDay, player_wins_per_day,
                                     final_player_value_split,
                                     computer_hand, temp_deck)

            playerTotalWins += player_wins_per_day
            pcTotalWins += pc_wins_per_day

            history["Day " + str(dayCnt)]["Round " + str(rnd_per_day)]["Money in pocket that day"] = MoneyInPocketPerDay
            history["Day " + str(dayCnt)]["Round " + str(rnd_per_day)]["Total money in pocket"] = totalMoneyInPocket + MoneyInPocketPerDay
            history["Day " + str(dayCnt)]["Round " + str(rnd_per_day)]["% win that day"] = (MoneyInPocketPerDay / initial_amount_per_day - 1) * 100
            history["Day " + str(dayCnt)]["Round " + str(rnd_per_day)]["% total win"] = (totalMoneyInPocket + MoneyInPocketPerDay /
                                                                                         (dayCnt * initial_amount_per_day)) * 100
            history["Day " + str(dayCnt)]["Round " + str(rnd_per_day)]["Player wins that day"] = player_wins_per_day
            history["Day " + str(dayCnt)]["Round " + str(rnd_per_day)]["PC wins that day"] = pc_wins_per_day
            history["Day " + str(dayCnt)]["Round " + str(rnd_per_day)]["Player total wins"] = playerTotalWins
            history["Day " + str(dayCnt)]["Round " + str(rnd_per_day)]["PC total wins"] = pcTotalWins


            # print(f"\nTotal rounds: {rnd}, Player {player_wins_per_day}:{pc_wins_per_day} PC, draws: {rnd - player_wins_per_day - pc_wins_per_day}")
            # print()

            if rnd_per_day == max_rounds_per_day or MoneyInPocketPerDay <= 0:
                break

        totalMoneyInPocket += MoneyInPocketPerDay
        if dayCnt == total_days:
            break

    return history, totalMoneyInPocket


def main():
    history, totalMoneyBack = playBlackjack()
    listOfDailyMoney = [history["Day " + str(day)]["Round " + str(rnd)]["Money in pocket that day"] for day in range(1, len(history.keys()) + 1)
                        for rnd in range(len(history["Day " + str(day)].keys()), len(history["Day " + str(day)].keys()) + 1)]

    listOfDailyMoneyPercentages = [(money / initial_amount_per_day - 1) * 100 for money in listOfDailyMoney]

    print(f"\nYou start with {initial_amount_per_day}$ every day")
    print(f"You go to the casino for {total_days} days")
    print(f"The initial amount you bet every round is {initial_bet_amount_per_round}$")
    print(f"The maximum rounds you can play every day is {max_rounds_per_day}")

    print(f"\nTotal money that you receive back is {totalMoneyBack}$ out of {initial_amount_per_day * total_days}$")
    print(f"Win % is {(totalMoneyBack / (initial_amount_per_day * total_days) - 1) * 100}%")

    # Absolute values
    mean_of_absolute = sum(listOfDailyMoney) / len(listOfDailyMoney)
    deviation_of_absolute = round(sqrt(sum([(i - mean_of_absolute) ** 2 for i in listOfDailyMoney]) / len(listOfDailyMoney)), 2)
    print("\nAbsolute Values")
    print(f"Average money you win back per day out of {initial_amount_per_day}$ is {mean_of_absolute}$")
    print(f"Variation of expected money per day is between {mean_of_absolute - deviation_of_absolute}$ and {mean_of_absolute + deviation_of_absolute}$")

    # Percentages
    mean_of_percentages = sum(listOfDailyMoneyPercentages) / len(listOfDailyMoneyPercentages)
    deviation_of_percentages = round(sqrt(sum([(i - mean_of_percentages) ** 2 for i in listOfDailyMoneyPercentages]) / len(listOfDailyMoneyPercentages)), 2)
    print("\nPercentages")
    print(f"Average daily % win is {mean_of_percentages}%")
    print(f"Variation of expected daily % win is {mean_of_percentages - deviation_of_percentages}% and {mean_of_percentages + deviation_of_percentages}%")

    if total_days > 10:
        columnsList = ["Day " + str(j) for j in range(1, 11)]
        rowsList = ["+ " + str(10 * i) + " days" for i in range(ceil(total_days / 10))]
    else:
        columnsList = ["Day " + str(j) for j in range(1, total_days)]
        rowsList = ["+ 0 days"]

    print()
    listOfDailyMoney = [str(number) + "$" for number in listOfDailyMoney]
    table(listOfDailyMoney, columnsList, rowsList)


main()
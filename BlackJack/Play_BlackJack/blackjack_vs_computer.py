# here is a simplified version of Blackjack, you can play against BlackJack and have the computer as a dealer,
# the program keeps track of the history of the game everytime it runs

# computer is the dealer, it must stand on 17 or above

# you can add as many decks as you want, simply by multiplying the global deck variable, i.e.
# deck = 8 * {(number, color) for number in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "jack", "queen", "king")
#               for color in ("heart", "spade", "club", "diamond")}

from random import choice
from copy import deepcopy

# globals
deck = {(number, color) for number in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "jack", "queen", "king")
        for color in ("heart", "spade", "club", "diamond")}


# functions
def yes_or_no() -> str:
    user_input = input("Type 'yes' or 'no': ").strip().lower()
    while True:
        if user_input not in ["yes", "no"]:
            print("\nThis is not a valid answer.")
            user_input = input("Type 'yes' or 'no': ").strip().lower()
        else:
            return user_input


# gives a random card from a deck
def give_random_card(my_deck: set) -> tuple:
    x = choice(list(my_deck))
    my_deck.remove(x)
    return x


# adds a value to an existing hand value tuple that contains two values of the hand
# the two values of the hand will be different only if the hand contains any aces
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


# it calculates the value of the hand, it always calculates two values, these two values will be different only
# if there is an ace in the hand
def hand_value(cards_set: set) -> tuple:
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


# checks whether the user decision is indeed 'hit me' or 'stand'
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


# it is the process of the player while they play
def player(my_deck: set):  # returns int or "Blackjack" if player has value 21 with two cards only

    player_hand = [give_random_card(my_deck), give_random_card(my_deck)]
    # print(f"Deck has {len(my_deck)}")

    hand_value_tuple = hand_value(set(player_hand))
    print_cards_and_value(hand_value_tuple, player_hand, "player")

    if 21 in hand_value_tuple:
        print("\nYou have Blackjack!!!")
        return "Blackjack"

    while True:
        if get_input_and_check_it() == "stand":
            if max(hand_value_tuple) <= 21:
                print(f"\nFinal value of player hand is {max(hand_value_tuple)}")
                return max(hand_value_tuple)
            else:
                print(f"\nFinal value of player hand is {hand_value_tuple[0]}")
                return hand_value_tuple[0]
        else:
            x = give_random_card(my_deck)
            # print(f"Deck has {len(my_deck)}")
            player_hand.append(x)
            hand_value_tuple = add_value_to_existing_hand(x, hand_value_tuple)
            print_cards_and_value(hand_value_tuple, player_hand, "player")

            if min(hand_value_tuple) > 21:
                return min(hand_value_tuple)
            elif 21 in hand_value_tuple:
                return hand_value_tuple[1]


# simulates the dealer / computer play style
def computer(computer_hand: list, my_deck: set,
             value_to_beat: int):  # returns int or "Blackjack" if PC has value 21 with two cards only
    computer_value = hand_value(set(computer_hand))
    print_cards_and_value(computer_value, computer_hand, "PC")
    if 21 in computer_value:
        return "Blackjack"

    while True:
        if computer_value[1] <= 21:
            if computer_value[1] in range(17, 21 + 1):
                return computer_value[1]
            else:
                x = give_random_card(my_deck)
                # print(f"Deck has {len(my_deck)}")
                computer_hand.append(x)
                computer_value = add_value_to_existing_hand(x, computer_value)
                print_cards_and_value(computer_value, computer_hand, "PC")
        elif computer_value[0] <= 21:
            if computer_value[0] in range(17, 21 + 1):
                return computer_value[0]
            else:
                x = give_random_card(my_deck)
                # print(f"Deck has {len(my_deck)}")
                computer_hand.append(x)
                computer_value = add_value_to_existing_hand(x, computer_value)
                print_cards_and_value(computer_value, computer_hand, "PC")
        else:
            return min(computer_value)


# main
def main():
    rnd = 0
    player_total_wins = 0
    pc_total_wins = 0

    while True:
        rnd += 1
        print(f"Round: {rnd}")
        temp_deck = deepcopy(deck)
        computer_hand = [give_random_card(temp_deck), give_random_card(temp_deck)]
        print(f"\nPC has (########) {computer_hand[1]}")
        final_player_value = player(temp_deck)

        if final_player_value != "Blackjack" and final_player_value > 21:
            pc_total_wins += 1
            print("\nYou lost unfortunately, your cards value is over 21...")
        else:
            final_computer_value = computer(computer_hand, temp_deck, final_player_value)
            # print(f"Deck has {len(temp_deck)} cards")

            if final_player_value == "Blackjack":
                if final_computer_value != "Blackjack":
                    player_total_wins += 1
                    print("\nYou win!!!! You have Blackjack and dealer doesn't!!!")
                else:
                    print("\nUnbelievable...PC has also Blackjack...It's a draw...")
            elif final_computer_value == "Blackjack":
                if final_player_value != "Blackjack":
                    pc_total_wins += 1
                    print("\nAh you lost... PC has blackjack and you don't...")
            else:
                if final_player_value <= 21 and final_computer_value <= 21:
                    if final_player_value > final_computer_value:
                        player_total_wins += 1
                        print("\nYou win!!!")
                    elif final_player_value < final_computer_value:
                        pc_total_wins += 1
                        print("\nAhh you lost...")
                    else:
                        print("\nIt's a draw...")
                elif final_player_value <= 21:
                    player_total_wins += 1
                    print("\nYou win!!!")
                elif final_computer_value <= 21:
                    pc_total_wins += 1
                    print("\nAhh you lost...")

        print(f"\nTotal rounds: {rnd}, Player {player_total_wins}:{pc_total_wins} PC, draws: {rnd - player_total_wins - pc_total_wins}")

        print("\nDo you want to continue?")
        if yes_or_no() == "no":
            break

        print()


main()
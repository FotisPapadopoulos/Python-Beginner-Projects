# the following program picks randomly 5 cards from a 52-card deck and checks whether the hand is a straight or
# an aces full

# definitions
# straight: Any five consecutive cards of different suits
# aces full: the 5 - card hand contains 4 aces

from random import randrange

# globals
colors = {"spade", "heart", "club", "diamond"}
ranks = (2, 3, 4, 5, 6, 7, 8, 9, 10, "jack", "queen", "king", "ace")

deck = set()
for rank in ranks:
    for color in colors:
        deck.add((rank, color))


# functions

# it gives the rank hierarchy order of a card represented as a tuple i.e. (2, "spade")
def rank_order(card):
    rank = card[0]
    return ranks.index(rank)


# checks whether an iterable consisted of cards is a straight
def is_straight(cards) -> bool:
    sorted_cards = sorted(cards, key=rank_order)
    rank_indices = [rank_order(card) for card in sorted_cards]

    if rank_indices == [0, 1, 2, 3, 12]:  # it is equivalent to having 2, 3, 4, 5 and an ace in cards
        return True
    return all(rank_indices[i] + 1 == rank_indices[i + 1] for i in range(len(rank_indices) - 1))


def is_aces_full(cards) -> bool:
    cnt = 0
    for card in cards:
        if card[0] == "ace":
            cnt += 1

    if cnt == 4:
        return True
    else:
        return False


# it selects randomly 5 cards from a 52 - card deck using any of the three aforementioned functions
def pick_randomly_5_cards() -> set:
    myDeck = deck.copy()
    array = set()
    myList = list(myDeck)
    for _ in range(5):
        x = myList.pop(randrange(len(myList)))
        array.add(x)
    return array


# main
def main():
    cards = pick_randomly_5_cards()
    if is_straight(cards):
        print(f"\nYour hand is: {cards}")
        print("\nCongratulations, you have a straight.")
    elif is_aces_full(cards):
        print(f"\nYour hand is: {cards}")
        print("\nCongratulations, you have a aces full.")
    else:
        print(f"\nYour hand is: {cards}")
        print("\nYou don't have straight or aces full.")


main()
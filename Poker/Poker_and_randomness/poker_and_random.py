# The following code aims to check if the functions set.pop(), randrange(), and choice() do actually produce random
# selections of elements from a set.

# Specifically, we will select 5 random cards from a full deck (52 cards) using each of the aforementioned methods
# and check if these 5 cards form a straight.

# Now, the possible straights of 5 cards from a 52-card deck are x = 10,240, while the possible combinations of 5 cards
# from a 52-card deck are y = 2,598,960,
# Therefore the probability of having a straight is x / y = 0.00394 or 0.394%.

# So, we will run several thousand rounds and see if all three functions produce a straight with a probability close
# to 0.394%

# !!! The deck contains 52 cards and gets reset every time we pick 5 cards randomly !!!
# straight: Any five consecutive cards

from random import randrange, choice

# globals
colors = {"spade", "heart", "club", "diamond"}
ranks = (2, 3, 4, 5, 6, 7, 8, 9, 10, "jack", "queen", "king", "ace")

deck = set()
for rank in ranks:
    for color in colors:
        deck.add((rank, color))

rounds = 10000
methods = {"pop": 0, "randrange": 0, "choice": 0}


# functions

# it gives the rank hierarchy order of a card represented as a tuple i.e. (2, "spade")
def rank_order(card):
    rank = card[0]
    return ranks.index(rank)


# checks whether an iterable consisted of cards is a straight
def is_straight(cards):
    sorted_cards = sorted(cards, key=rank_order)
    rank_indices = [rank_order(card) for card in sorted_cards]

    if rank_indices == [0, 1, 2, 3, 12]:  # it is equivalent to having 2, 3, 4, 5 and an ace in cards
        return True
    return all(rank_indices[i] + 1 == rank_indices[i + 1] for i in range(len(rank_indices) - 1))


# it selects randomly 5 cards from a 52 - card deck using any of the three aforementioned functions
def pick_5_cards(method: str) -> set:
    myDeck = deck.copy()
    array = set()
    if method == "pop":
        for _ in range(5):
            array.add(myDeck.pop())
        return array
    elif method == "randrange":
        myList = list(myDeck)
        for _ in range(5):
            x = myList.pop(randrange(len(myList)))
            array.add(x)
        return array
    else: # method == "choice"
        myList = list(myDeck)
        for _ in range(5):
            x = choice(myList)
            myList.remove(x)
            array.add(x)
        return array


# main
def main():
    for _ in range(10000):
        if is_straight(pick_5_cards("pop")):
            methods["pop"] += 1

        if is_straight(pick_5_cards("randrange")):
            methods["randrange"] += 1

        if is_straight(pick_5_cards("choice")):
            methods["choice"] += 1

    print(f"Probability of straight is 0.394%")

    print(f"set.pop() function 'straight' probability  : {(methods["pop"] / rounds) * 100}% ")
    print(f"randrange() function 'straight' probability: {(methods["randrange"] / rounds) * 100}% ")
    print(f"choice() function 'straight' probability   : {(methods["choice"] / rounds) * 100}% ", end="\n\n")

    # the following loop shows that set.pop() gives us the same cards every time we run it
    for _ in range(20):
        print(pick_5_cards("pop"))


main()


# we see that randrange and choice work perfectly, however pop function doesn't behave as we would like
# instead it gives us the same 5 cards in every loop / round

# the number of possible k combinations from n objects where order doesn't matter, where n and k are integers and 0<=k<=n,
# equals to n!/(k!(n-k)!)
# therefore number of 5 combinations from 52 cards where order doesn't matter, equals to 52!/(5!(47!)) = 2.598.960

# the number of possible straights in a 52 card set equals to 10 * 4^5 = 10.240
# therefore the possibility of getting 5 straights is 2.598.960 / 10.240 which is approximately 0,00394.

# therefore it happens 0,00394 times every 1 time or 1 time every approximately 254 times
# therefore it happens 100 times every approximately 25400 times
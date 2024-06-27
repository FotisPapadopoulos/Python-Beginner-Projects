# play rock, paper, scissors against the computer

from random import choice

# globals
# do not change
power_values = {"scissors": 0, "rock": 1, "paper": 2}
history = {}
player_total_wins = 0
pc_total_wins = 0
draws = 0
# change wins_to_reach according to how many wins one has to get to end the game
wins_to_reach = 3

# functions


# it returns 'rock', 'paper' or 'scissors'
def player_picks_their_power():
    user_input = input("\nType your power ('rock', 'paper' or 'scissors'): ").lower().strip()
    while user_input not in ["rock", "paper", "scissors"]:
        user_input = input("Not a valid choice. Choose your power (rock, paper or scissors): ")

    return user_input


# it returns 'rock', 'paper' or 'scissors'
def pc_picks_their_power():
    return choice(list(power_values.keys()))


# it returns 'pc', 'player' or 'draw'
def check_who_wins(player_power: str, pc_power: str) -> str:
    player_value = power_values[player_power]
    pc_value = power_values[pc_power]

    if player_value - pc_value == 0:
        return "draw"
    elif player_value - pc_value == 2 or player_value - pc_value == -1:
        return "pc"
    else:
        return "player"


def save_round_history(winner: str, player_power: str, pc_power: str):
    myDict = {}

    global player_total_wins, pc_total_wins, draws

    myDict["Winner"] = winner
    myDict["Player power"] = player_power
    myDict["PC power"] = pc_power
    myDict["Player total wins"] = player_total_wins
    myDict["PC total wins"] = pc_total_wins

    if winner == "player":
        player_total_wins += 1
        myDict["Player total wins"] += 1
    elif winner == "pc":
        pc_total_wins += 1
        myDict["PC total wins"] += 1
    else:
        draws += 1

    return myDict


def save_history(round:int, round_history:dict):
    history["Round " + str(round)] = round_history


def print_round_winner_and_score(round_history: dict):
    if round_history["Winner"] != "draw":
        print(f"\n{round_history["Winner"]} wins!!!")
    else:  # draw
        print("\nIt's a draw...")
    print(f"Player power: {round_history["Player power"]}, PC power: {round_history["PC power"]}")
    print(f"Player {player_total_wins}:{pc_total_wins} PC, draws: {draws}")


# prints a 2-dimensional table, to be used in print_history() function
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


def print_history(history: dict):
    rows_titles = list(history.keys())
    columns_titles = ["Player power", "Pc power", "Winner", "Score"]

    data = []
    for round_history in history.values():
        data.append(round_history["Player power"])
        data.append(round_history["PC power"])
        data.append(round_history["Winner"])

        score = f"Player {round_history["Player total wins"]}:{round_history["PC total wins"]} PC"
        data.append(score)

    print(end="\n\n")
    table(data, columns_titles, rows_titles)


# main
def main():
    rnd = 0
    while player_total_wins < 3 and pc_total_wins < 3:
        rnd += 1
        print(f"\nRound {rnd}")

        player_power = player_picks_their_power()
        pc_power = pc_picks_their_power()

        winner = check_who_wins(player_power, pc_power)
        round_history = save_round_history(winner, player_power, pc_power)
        save_history(rnd, round_history)

        print_round_winner_and_score(round_history)
    else:
        print_history(history)


main()




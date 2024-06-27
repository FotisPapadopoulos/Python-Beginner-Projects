# LOTTO is a famous lottery competition that takes place in Greece
# the prize could reach to multiple hundred thousand euros
# the following program's purpose is to find the probability of winning LOTTO with one and only guess
# LOTTO consists of 49 numbers and the winner is the one that guesses correctly the winning 6-number combination,
# obviously order doesn't matter

# C(n, k) = C(n - 1, k - 1) + C(n - 1, k) if n > k
# C(n, k) = 1 if k = n
# C(n, k) = n if k = 1
# the above calculations is about possible k combinations from n elements WITHOUT repositioning, order Doesn't matter

# functions
def C(n: int, k: int) -> int:
    if n >= k:
        if k == 1:
            return n
        elif n == k:
            return 1
        else:
            return C(n - 1, k - 1) + C(n - 1, k)
    else:  # k > n => 0 possible combinations
        return 0


# main
def main():
    print(f"\nThe chance of winning LOTTO is 1 in {C(49, 6)}")  # possible combinations from lotto


main()
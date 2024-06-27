# the following program tells you if the number is even, odd, prime, square and cube for the first N numbers

# globals
N = 1000


# functions
def is_odd(number):
    return number % 2 == 1


def is_even(number):
    return number % 2 == 0


def is_prime(number):
    if number <= 1:
        return True
    else:
        for i in range(2, int(number / 2)):
            if number % i == 0:
                return False
        else:
            return True


def is_square(number):
    if number >= 0:
        if 0 == (number ** (1 / 2)) % 1:
            return True
        else:
            return False
    else:
        return False


def is_cube(number):
    if number >= 0:
        if 0 == (number ** (1 / 3)) % 1:
            return True
        else:
            return False
    else:
        return False


def print_table(N):
    print("\t".expandtabs(len(str(N)) + 2), "|", f"is odd".center(11), "|", f"is even".center(11), "|",
          f"is prime".center(11),
          "|", f"is square".center(11), "|", f"is cube".center(11), "|", sep="")
    print("-" * 66)
    for i in range(1, N + 1):
        print((str(i) + "\t").expandtabs(len(str(N)) + 2), "|", str(is_odd(i)).center(11), "|",
              str(is_even(i)).center(11),
              "|", str(is_prime(i)).center(11), "|", str(is_square(i)).center(11), "|", str(is_cube(i)).center(11), "|",
              sep="", end=" ")
        if is_square(i):
            print(f"square root: {int(i ** (1 / 2))}", end="  ")
        if is_cube(i):
            print(f"cube root : {int(i ** (1 / 3))}", end="")
        print()
        print("-" * 66)


def main():
    print_table(N)


main()
#  the following program includes a binary search function, and checks if it works correctly

# globals
orderedList = [number for number in range(1, 20 + 1)]


# functions
def binary_search(myList: list,
                  element) -> int:  # keep in mind that the arguments should be an ORDERED list and a number
    if len(myList) > 0:
        pos = int(len(myList) / 2)
        if myList[pos] == element:
            return pos
        else:
            if myList[pos] > element:
                x = binary_search(myList[:pos], element)
                return x if x != -1 else -1
            else:  # myList[pos] < element
                x = binary_search(myList[pos + 1:], element)
                return pos + 1 + x if x != -1 else -1
    else:
        return -1


# main
def main():
    for number in orderedList:
        print(f"Number {number} is in position {binary_search(orderedList, number)}")

    print()
    x, y, z = 10000, -1, 10.5  # three numbers that are bigger, smaller and in between for every element of orderedList
    print(f"Number {x} is in position {binary_search(orderedList, x)}")
    print(f"Number {y} is in position {binary_search(orderedList, y)}")
    print(f"Number {z} is in position {binary_search(orderedList, z)}")


main()
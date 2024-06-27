# created a function that sorts out a list using the insertion sorting technique and checked if it works

from random import randrange

# globals
start = 1
stop = 100
howManyNumbers = 20
randomList = []
for _ in range(howManyNumbers):
    randomList.append(randrange(start, stop + 1))


# functions
def insertion_sorting_loop(argList, descending=False):
    myList = argList[:]
    if not descending:
        for i in range(1, len(myList)):
            for j in range(i, 0, -1):
                if myList[j] < myList[j - 1]:
                    myList[j], myList[j - 1] = myList[j - 1], myList[j]
                else:
                    break
        else:
            return myList
    else:
        for i in range(1, len(myList)):
            for j in range(i, 0, -1):
                if myList[j] > myList[j - 1]:
                    myList[j], myList[j - 1] = myList[j - 1], myList[j]
                else:
                    break
        else:
            return myList


# main
def main():
    print(f"Initial List: {randomList}")
    print(f"Sorted List in ascending order : {insertion_sorting_loop(randomList)}")
    print(f"Sorted List in descending order: {insertion_sorting_loop(randomList, descending=True)}")


main()
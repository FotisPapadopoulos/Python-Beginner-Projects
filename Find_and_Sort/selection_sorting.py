# created a function that sorts out a list using the selection sorting technique and checked if it works

from random import randrange

# globals
myList = []
for a in range(1, 10 + 1):
    myList.append(randrange(0, 10 + 1))


# functions
def selection_sort(array, descending=False) -> list:
    temp_List = array[:]
    if not descending:
        for i in range(0, len(temp_List) - 1):
            x = min(temp_List[i: len(temp_List)])
            minimum_pos = temp_List[i: len(temp_List)].index(x) + i
            temp_List[minimum_pos], temp_List[i] = temp_List[i], temp_List[minimum_pos]
    else:  # elif descending
        for i in range(0, len(temp_List) - 1):
            x = max(temp_List[i: len(temp_List)])
            maximum_pos = temp_List[i: len(temp_List)].index(x) + i
            temp_List[maximum_pos], temp_List[i] = temp_List[i], temp_List[maximum_pos]

    return temp_List


# main
def main():
    print(f"Initial List: {myList}")
    print(f"Sorted list in ascending order : {selection_sort(myList)}")
    print(f"Sorted list in descending order: {selection_sort(myList, descending=True)}")


main()

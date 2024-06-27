# the following program prints random numbers as a 2-dimensional table
# you get to decide how many numbers you want and the dimensions (rows and columns) of the 2-dimensional table

from random import randrange

# globals

end_number = 10000  # this is maximum number it can be printed
rows = 23  # how many rows the table will have
cols = 222  # how many columns the table will have, rows * columns gives the total numbers that will be printed


# creation of the 2-dimensional list
def create_list():
    my_list = []
    for row in range(rows):
        my_list.append([])
        for _ in range(cols):
            my_list[row].append(randrange(end_number + 1))

    max_number_of_digits = len(str(end_number + 1 - 1))
    return my_list


# creation of the printed output
def print_table(my_list):
    number_of_spaces_before_every_divider_line = (len(str(rows)) + 1)
    max_number_of_digits = len(str(end_number + 1 - 1))

    for row in range(rows * 2, -1, -1):
        if row % 2 == 0:
            print(" " * number_of_spaces_before_every_divider_line + (
                        "+" + "-" * (max_number_of_digits + 1)) * cols + "+")
        else:
            number_of_spaces_trailing_every_line_number = number_of_spaces_before_every_divider_line - len(
                str(row // 2))
            print(str(row // 2) + " " * number_of_spaces_trailing_every_line_number, end="")
            for col in range(cols):
                number = my_list[int(row / 2)][col]
                string_for_numbers = "|" + str(number) + "\t"
                print_string = string_for_numbers.expandtabs(max_number_of_digits + 2)
                print(print_string, end="")
            print("|")


# main
def main():
    print_table(create_list())


main()
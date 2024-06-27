# the following program counts how many times each alphabetic character appears on a given string
# special characters and spaces are removed, there is no distinction between upper and lower case characters

# globals

text = "How the hell could a person enjoy being awakened at 6:30AM, by \
an alarm clock, leap out of bed, dress, force-feed, shit, piss, brush \
teeth and hair, and fight traffic to get to a place where essentially \
you made lots of money for somebody else and were asked to be \
grateful for the opportunity to do so?"


# main
def main(my_string:str):
    # remove spaces and lower all characters

    my_string = "".join(my_string.split(" ")).lower()

    # create iterable argument for the translate function

    dict_of_string_replacements = {ord(":"): None, ord(","): None, ord("-"): None, ord("?"): None}

    # remove characters based on the dictionary above

    my_string = my_string.translate(dict_of_string_replacements)

    # create a set of the letters that exist in the string

    letters_set = {letter for letter in my_string if not letter.isnumeric()}

    dict_of_sums_for_each_char = {letter: 0 for letter in letters_set}

    # match the letters with their values of how many times they appear in the string

    for char in my_string:
        if not char.isnumeric():
            dict_of_sums_for_each_char[char] += 1

    # sort the dictionary based on its values

    sorted_temp_list = sorted(dict_of_sums_for_each_char.items(), key=lambda x: x[1], reverse=True)
    max_value_of_dict = sorted_temp_list[0][1]
    dict_of_sums_for_each_char = dict(sorted_temp_list)

    # print the output

    for key, value in dict_of_sums_for_each_char.items():
        if value != 1:
            print(f"{key}: {value}" + "\t".expandtabs(len(str(max_value_of_dict)) - len(str(value))) + " times")
        else:
            print(f"{key}: {value}" + "\t".expandtabs(len(str(max_value_of_dict)) - len(str(value))) + " time")


main(text)
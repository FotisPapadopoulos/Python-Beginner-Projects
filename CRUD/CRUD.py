# In computer programming, create, read, update, and delete (CRUD) are the four basic operations of persistent storage
# this program is a simple simulation of how CRUD works


# globals
students_dict = {1000: {"Name": "Chris",
                        "Surname": "Black",
                        "FatherName": "Lebron",
                        "Age": 8,
                        "Class": 3,
                        "PoliceID": "EWR1256",
                        },
                 1001: {"Name": "Maria",
                        "Surname": "Black",
                        "FatherName": "Kevin",
                        "Age": 10,
                        "Class": 5,
                        "PoliceID": "ADF1674",
                        },
                 1002: {"Name": "Peter",
                        "Surname": "Alexander",
                        "FatherName": "Steph",
                        "Age": 7,
                        "Class": 2,
                        "PoliceID": "-",
                        }
                 }


# functions
def yes_or_no() -> str:
    user_input = input("Type 'yes' or 'no': ").strip().lower()
    while True:
        if user_input not in ["yes", "no"]:
            print("\nThis is not a valid answer.")
            user_input = input("Type 'yes' or 'no': ").strip().lower()
        else:
            return user_input


def check_if_int(string_for_input: str, start=None, end=None) -> int:
    # create a string parenthesis depicting the range of numbers allowed to be used in input prints for user
    if start is not None and end is not None:
        parenthesis_of_numbers = f" ({start}-{end})"
    elif start is not None:
        parenthesis_of_numbers = f" ({start}-∞)"
    elif end is not None:
        parenthesis_of_numbers = f" (-∞ - {end})"
    else:
        parenthesis_of_numbers = ""

    user_input = input(f"\nPlease type {string_for_input} as an integer number{parenthesis_of_numbers}: ")
    while True:
        try:
            int(user_input)
            # create the condition required to check if number is in the requested range
            if start is not None and end is not None:
                is_number_in_requested_range = int(user_input) in range(start, end + 1)
            elif start is not None:
                is_number_in_requested_range = int(user_input) >= start
            elif end is not None:
                is_number_in_requested_range = int(user_input) <= end
            else:
                is_number_in_requested_range = True

            if not is_number_in_requested_range:
                print("This is not an acceptable integer.")
                user_input = input(f"Please type {string_for_input} as an integer positive number{parenthesis_of_numbers}: ")
            else:
                return int(user_input)

        except ValueError:
            print("\nThis is is not an integer.")
            user_input = input(f"Please type {string_for_input} as an integer number{parenthesis_of_numbers}: ")


def check_if_only_letters(string_for_input: str) -> str:
    user_input = input(f"\nPlease type {string_for_input} (only letters allowed): ")

    while True:
        inputWithoutSpaces = "".join(user_input.split())
        if not inputWithoutSpaces.isalpha():
            print("\nYour input contains characters that are not letters")
            user_input = input(f"Please type {string_for_input} (only letters allowed): ")
        else:
            return user_input


def check_if_int_input_is_in_iterable(string_for_input: str, array) -> int:
    user_input = input(f"Please type {string_for_input}: ")
    while True:
        try:
            user_input = int(user_input)
            for element in array:
                if element == user_input:
                    return user_input
            else:
                print(f"\n{string_for_input.capitalize()} is not one of the available choices.")
                user_input = input(f"Please type {string_for_input}: ")
        except ValueError:
            print("\nThis is not an integer.")
            user_input = input(f"Please type {string_for_input}: ")


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

def check_if_policeID_is_acceptable() -> str: # it returns the accepted answer of the user as a string
    id_ = input(
        "\nPlease type your id (3 letters and 4 numbers without spaces) or type '-' if you don't have any: ").strip().upper()
    # checks whether id input has 3 letters and 4 numbers without spaces
    while True:
        if id_ == "-":
            break
        elif len(id_) != 7:
            print("This is not an acceptable input.")
            id_ = input(
                "Please type your id (3 letters and 4 numbers without spaces) or type '-' if you don't have any: ").strip().upper()
            break
        else:
            is_id_acceptable = True
            for pos in range(len(id_)):
                if pos < 3:
                    if not id_[pos].isalpha():
                        is_id_acceptable = False
                        break
                else:
                    if not id_[pos].isnumeric():
                        is_id_acceptable = False
            if is_id_acceptable:
                break
            else:
                print("This is not an acceptable input.")
                id_ = input(
                    "Please type your id (3 letters and 4 numbers without spaces) or type '-' if you don't have any: ").strip().upper()
    return id_


# find next available id from students dict
def next_id() -> int:
    return max(students_dict.keys()) + 1


# menu selection
def menu_selection() -> int:
    print("\nMain Menu")
    print("\nRegistration (1)\n" + "Print (2)\n" + "Information update (3)\n" + "Information deletion (4)\n" + "Exit (5)")
    return check_if_int("your selection", 1, 5)


# Registration
def create_pupil():
    while True:
        print("\nCreate a new pupil.")
        name = check_if_only_letters("your Name").strip().capitalize()
        surname = check_if_only_letters("your Surname").strip().capitalize()
        fathername = check_if_only_letters("your Father's name").strip().capitalize()

        # check if pupil exists and ask user if they want to continue with registration
        continue_with_registration = "yes"
        for key, value in students_dict.items():
            if value["Name"] == name and \
                    value["Surname"] == surname and \
                    value["FatherName"] == fathername:
                print("\nThere is already one student with the same details.")
                print(f"Name      : {value["Name"]}\n"
                      f"Surname   : {value["Surname"]}\n"
                      f"FatherName: {value["FatherName"]}\n"
                      f"Age       : {value["Age"]}\n"
                      f"Class     : {value["Class"]}\n"
                      f"ID        : {value["ID"]}")

                continue_with_registration = input("Do you still wish to continue with registration? Type 'yes' or 'no': ").strip().lower()
                while True:
                    if continue_with_registration != "yes" and continue_with_registration != "no":
                        continue_with_registration = input("Please type only 'yes' or 'no'.")
                    else:
                        break
        if continue_with_registration == "no":
            break

        age = check_if_int("your age", 5, 11)

        class_number = check_if_int("your class number", 1, 6)

        policeId = check_if_policeID_is_acceptable()

        # saves new entry on students dictionary
        students_dict[next_id()] = {"Name": name,
                                            "Surname": surname,
                                            "FatherName": fathername,
                                            "Age": age,
                                            "Class": class_number,
                                            "PoliceID": policeId
                                            }

        print("\nRegistration completed successfully!!!")
        print(f"Name      : {name}\n"
              f"Surname   : {surname}\n"
              f"FatherName: {fathername}\n"
              f"Age       : {age}\n"
              f"Class     : {class_number}\n"
              f"ID        : {policeId}")

        print("\nDo you want to create another new pupil?")
        user_decision = yes_or_no()

        if user_decision == "yes":
            continue
        else:
            break


def print_pupil():
    while True:
        print("\nPrint only 1 pupil (1)\n" + "Print all pupils (all features) (2)\n" + "Print all pupils (only names) (3)\n" + "Exit (4)")
        user_input = check_if_int("your selection", 1, 4)

        if user_input == 1:
            Id = check_if_int("the id you want to print", 1)
            print_1_pupil(Id)
        elif user_input == 2:
            print_all_pupils_all_features()
        elif user_input == 3:
            print_all_pupils_only_names()
        else:
            break


def print_1_pupil(myId: int):
    print()
    for number in students_dict.keys():
        if myId == number:
            # preparing inputs for my function table
            data = [number]
            columnsTitles = ["Internal Id", "Name", "Surname", "Father Name", "Age", "Class", "Police Id"]
            rowsTitles = ["Pupil 1"]
            for value in students_dict[number].values():
                data.append(value)

            table(data, columnsTitles, rowsTitles)
            return
    else:
        print("This Id doesn't exist...")


def print_all_pupils_all_features():
    print()
    if len(students_dict) > 0:
        data = []
        columnTitles = ["Internal Id", "Name", "Surname", "Father Name", "Age", "Class", "Police Id"]
        rowsTitles = []
        cnt = 0
        for key, pupilDictionary in students_dict.items():
            cnt += 1
            data.append(key)
            rowsTitles.append(f"Pupil {cnt}")
            for value in pupilDictionary.values():
                data.append(value)

        table(data, columnTitles, rowsTitles)
    else:
        print("There is no student entry...")


def print_all_pupils_only_names():
    print()
    if len(students_dict) > 0:
        data = []
        columnTitles = ["Full Name"]
        rowsTitles = []
        cnt = 0
        for key, pupilDictionary in students_dict.items():
            cnt += 1
            data.append(f"{pupilDictionary["Name"]} {pupilDictionary["FatherName"][0]}. {pupilDictionary["Surname"]}")
            rowsTitles.append(f"Pupil {cnt}")
        table(data, columnTitles, rowsTitles)


def search_pupil_by_surname(surname):  # it returns a list that contains tuples, each tuple has an InternalId and a dictionary containing the personal details of the pupil
    array = []
    for InternalId, pupilDict in students_dict.items():
        if pupilDict["Surname"] == surname:
            array.append((InternalId, pupilDict))


def print_pupil_with_2_columns_only(internalID: int):
    print(f"Name         : {students_dict[internalID]["Name"]}\n"
          f"Surname      : {students_dict[internalID]["Surname"]}\n"
          f"Father's Name: {students_dict[internalID]["FatherName"]}\n"
          f"Age          : {students_dict[internalID]["Age"]}\n"
          f"Class        : {students_dict[internalID]["Class"]}\n"
          f"ID           : {students_dict[internalID]["PoliceID"]}")


# the following function is to be used in the 'update' function
def change_values_in_existing_internal_id(internalID: int):
    print("\nDo you want to change by order one to one (1) or by selection (2)?", end="")
    user_decision = check_if_int("your decision", 1, 2)
    if user_decision == 1:
        for key in students_dict[internalID].keys():

            if key not in ["FatherName", "PoliceID"]:
                print(f"\nDo you want to change the {key}?")
                user_decision = yes_or_no()

                if user_decision == "yes":
                    if key in ["Name", "Surname"]:  # Fathername is not included because the key is not ready for print
                        students_dict[internalID][key] = check_if_only_letters(f"the {key}")
                    elif key == "Age":
                        students_dict[internalID][key] = check_if_int("your age", 5, 11)
                    else:  # key == "Class"
                        students_dict[internalID][key] = check_if_int("your class number", 1, 6)
                else:  # user_decision == no
                    continue

            elif key == "FatherName":
                print(f"\nDo you want to change the {key}?")
                user_decision = yes_or_no()

                if user_decision == "yes":
                    students_dict[internalID][key] = check_if_only_letters("the Father's name")
                else:  # user_decision == no
                    continue

            else:  # key == PoliceID
                print(f"\nDo you want to change the {key}?")
                user_decision = yes_or_no()

                if user_decision == "yes":
                    students_dict[internalID][key] = check_if_policeID_is_acceptable()
                else:  # user_decision == no
                    continue

        print("\nUpdate completed successfully!!!")
        print_pupil_with_2_columns_only(internalID)
    else:  # user_decision == 2
        while True:
            print("\nName (1)\n" + "Surname (2)\n" + "Father's name (3)\n" + "Age (4)\n" + "Class (5)\n" + "Police ID (6)")
            user_decision = check_if_int("your selection", 1, 6)

            if user_decision == 1:
                students_dict[internalID]["Name"] = check_if_only_letters(f"the Name")
            elif user_decision == 2:
                students_dict[internalID]["Surname"] = check_if_only_letters(f"the Surname")
            elif user_decision == 3:
                students_dict[internalID]["FatherName"] = check_if_only_letters("the Father's name")
            elif user_decision == 4:
                students_dict[internalID]["Age"] = check_if_int("your age", 5, 11)
            elif user_decision == 5:
                students_dict[internalID]["Class"] = check_if_int("your class number", 1, 6)
            else:  # user_decision == 6
                students_dict[internalID]["PoliceID"] = check_if_policeID_is_acceptable()

            print("\nUpdate completed successfully!!!")
            print_pupil_with_2_columns_only(internalID)

            print("\nDo you want to change another information on the existing pupil?")
            user_decision = yes_or_no()
            if user_decision == "yes":
                continue
            else:  # user_decision == no
                break


def update():

    while True:
        print("\nUpdate Information on existing pupil.")
        print("Search by Surname (1) or by Internal ID (2)")
        user_input = check_if_int("the searching process you wish", 1, 2)

        if user_input == 1:
            user_surname_input = input("Please type the Surname: ").strip().capitalize()
            list_of_same_surnames = [] # it will contain tuples that contain the Internal ID and the personal dictionary of pupil's information
            for internalID, pupilDict in students_dict.items():
                if pupilDict["Surname"] == user_surname_input:
                    list_of_same_surnames.append((internalID, pupilDict))

            if len(list_of_same_surnames) == 0:
                print(f"\nThere is no student registered with the surname: {user_surname_input}")
            elif len(list_of_same_surnames) == 1:
                internalID = list_of_same_surnames[0][0]

                print("\nStudent was found.")
                print_pupil_with_2_columns_only(internalID)

                change_values_in_existing_internal_id(internalID)

            else:  # len(list_of_same_surnames) > 1
                print(f"\nThere are {len(list_of_same_surnames)} students found with that surname:")
                cnt = 0

                list_of_available_internal_IDs = []
                for element in list_of_same_surnames:
                    internalID = element[0]
                    list_of_available_internal_IDs.append(internalID)
                    cnt += 1
                    print(f"\nStudent no. {cnt}")
                    print(f"Internal ID  : {internalID}")
                    print_pupil_with_2_columns_only(internalID)

                print()
                user_pick = check_if_int_input_is_in_iterable("the internal ID of the pupil you want to update",
                                                              list_of_available_internal_IDs)

                internalID = user_pick
                change_values_in_existing_internal_id(internalID)
        else:  # user_input == 2, search by Internal ID
            internalID_input = check_if_int("the Internal ID of the pupil", 1)
            for key in students_dict.keys():
                if internalID_input == key:

                    print("\nStudent was found.")
                    print_pupil_with_2_columns_only(key)

                    change_values_in_existing_internal_id(key)
                    break
            else:
                print("\nInternal ID was not found")

        print("\nDo you want to update more information on existing pupils?")
        user_decision = yes_or_no()

        if user_decision == "yes":
            continue
        else:
            break


def delete_pupil_by_id(pupil_id):
    print_1_pupil(pupil_id)
    del students_dict[pupil_id]
    print("\nStudent was deleted")


def delete_process():
    while True:
        print("\nDo you want to delete by id (1) or by surname (2) or exit (3)?")
        user_choice = check_if_int("the process you want to follow", 1, 3)

        if user_choice == 1:  # delete by id
            ID = check_if_int("id you want to delete")

            if ID in students_dict.keys():  # student found
                delete_pupil_by_id(ID)

            else:  # there is no student with that specific ID
                print(f"\nThere is no student with ID equal to {ID}.")

        elif user_choice == 2:  # delete by surname
            surname = input("\nPlease type the surname: ").strip().lower()
            list_of_ids_with_the_same_surname = []
            for ID in students_dict.keys():
                if students_dict[ID]["Surname"].lower() == surname:
                    list_of_ids_with_the_same_surname.append(ID)

            l = len(list_of_ids_with_the_same_surname)
            if l == 0:  # no student found with that specific surname
                print(f"\nThere is no student named '{surname.capitalize()}'")

            elif l == 1:  # only one student found with that specific surname
                delete_pupil_by_id(list_of_ids_with_the_same_surname[0])

            else:  # multiple students found with that specific surname
                print("\nMore than 1 students were found.")
                for pos in range(0, l):
                    print(f"\nStudent no. {pos + 1}")
                    print_1_pupil(list_of_ids_with_the_same_surname[pos])

                print("\nDo you want to delete any of the above students?")
                user_yes_or_no = yes_or_no()

                if user_yes_or_no == "yes":  # delete student
                    user_pick = check_if_int("the number of the student you want to delete", 1,\
                                             len(list_of_ids_with_the_same_surname))
                    delete_pupil_by_id(list_of_ids_with_the_same_surname[user_pick - 1])

                else:  # user changed their mind, no deletion
                    pass
        elif user_choice == 3:  # exit
            return


# main
def main():
    while True:
        user_choice = menu_selection()
        if user_choice == 1:
            create_pupil()
        elif user_choice == 2:
            print_pupil()
        elif user_choice == 3:
            update()
        elif user_choice == 4:
            delete_process()
        else:
            print("\nGoodbye!!!")
            break


main()

# STRUCTURE OF THE PROCESS

# if menu_selection == 1 (create_pupil):
#     pass

# elif menu_selection == 2 (print_pupil):

#     if user_input == 1 (print_1_pupil):
#       pass
#     elif user_input == 2 (print_all_pupils_features):
#       pass
#     elif user_input == 3 (print_pupils_only_names):
#       pass

# elif menu_selection == 3 (update):

#       if user_input == 1 (search by surname):
#           no student found
#           one student found
#           multiple students found

#       elif user_input == 2 (search by ID):
#           ID found
#           ID wasn't found

# elif menu_selection == "information deletion":

#       if user_input == 1:  (delete by id)
#           id exists:
#           id doesn't exist

#       elif user_input == 2: (delete by surname)
#           surname doesn't exist
#           only one surname exists
#           multiple surnames exist

#       elif user_input == 3:
#           exit

# elif menu_selection == "exit":
#     print("Goodbye!!!")

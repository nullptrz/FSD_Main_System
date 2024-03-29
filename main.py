import datetime
import json
import os
from colorama import Fore, Back
from colorama import init

# Clears commandline screen for windows

init()

def clear_screen():
    def clear(): return os.system('cls')
    clear()

# Returns Time of the trip


def get_time():
    while (True):
        clear_screen()
        print_purchasing_header()
        try:
            time = int(input("""Enter time of departure (24-hour):

        1. 10:00
        2. 11:00
        3. 12:00
        4. 13:00
        5. 14:00
        6. 15:00
        7. 16:00
        8. 17:00\n\nEnter selection: """))
            if (time == 1):
                return 10
            elif (time == 2):
                return 11
            elif (time == 3):
                return 12
            elif (time == 4):
                return 13
            elif (time == 5):
                return 14
            elif (time == 6):
                return 15
            elif (time == 7):
                return 16
            elif (time == 8):
                return 17
            else:
                input(
                    "Please enter valid choice.. press [Enter] to continue . . . ")

        except ValueError:
            input("Please Enter a Number only! Press [Enter] to try again. .")

# Returns destination for the trip


def get_destination():
    while (True):
        clear_screen()
        print_purchasing_header()
        try:
            destination_choice = int(input("""Select your destination :

        1.Penang - Langkawi
        2.Langkawi - Penang\n\nEnter selection :"""))

            destination = None
            if (destination_choice == 1):
                destination = "Langkawi"
                return destination
            elif (destination_choice == 2):
                destination = "Penang"
                return destination
            else:
                input("Invalid Number...Press [Enter] to try again. .")
        except ValueError:
            input("Please enter a Number only! Press [Enter] to try again. . ")

# Returns the name of the customer


def get_name():
    while (True):
        customer_f_name = input("Enter your first name: ")
        customer_m_name = input(
            "Enter your middle name(if no middle name leave blank): ")
        customer_l_name = input("Enter your last name: ")
        customer_name = customer_f_name + " " + customer_m_name + " " + customer_l_name
        if customer_f_name.isalpha() and customer_l_name.isalpha():
            return customer_name

# Create list of tuples that contains (1st trip time, 2nd trip time)


def create_timeslot():
    time_slot = []

    for time in range(10, 18, 1):
        time_slot.append((time - 9, time))

    return time_slot

# Creates list with [source, destination, (different time slots)]


def create_schedule_penang(time_slot):
    schedule_penang = []

    for trip_penang in range(0, 8, 1):
        schedule_penang.append(["Langkawi", "Penang", time_slot[trip_penang]])

    return schedule_penang

# Creates list with [source, destination, (different time slots)]
# This Function can be generalized to allow the user to create
# Schedule for more than one destination


def create_schedule_langkawi(time_slot):
    schedule_langkawi = []

    for trip_langkawi in range(0, 8, 1):
        schedule_langkawi.append(
            ["Penang", "Langkawi", time_slot[trip_langkawi]])

    return schedule_langkawi

# Creates a mapping of ferry number to schedules
# of different destinations


def create_ferry_schedule(schedule_langkawi, schedule_penang):
    ferry_schedule = {}

    for item in range(0, 8, 1):
        ferry_schedule['FERRY' + " " + str(item + 1)] = schedule_langkawi[item]
        ferry_schedule['FERRY' + " " + str(item + 9)] = schedule_penang[item]

    return ferry_schedule

# Creates dictionary containing seating arrangement
# Key = Seat Number and Value = Booked[1]/Unbooked[0]
# Initially all seats are unbooked


def init_ferry():
    ferry = {}
    # Could replace 11 by N to accommodate more seats
    for business_seats in range(1, 11, 1):
        if business_seats >= 10:
            business_seats = 'B' + str(business_seats)
        else:
            business_seats = 'B0' + str(business_seats)
        ferry[business_seats] = 0
    # Could replace 40 by M to accommodate more seats
    for economy_seats in range(1, 41, 1):
        if economy_seats < 10:
            economy_seats = 'E0' + str(economy_seats)
        else:
            economy_seats = 'E' + str(economy_seats)
        ferry[economy_seats] = 0
    return ferry

# Creates a list of ferries containing dictionaries
# created by init_ferry function
# Hardcoded to create 8 Ferries only


def create_ferry_list(ferry):
    list_of_ferry = {}
    # Could replace 9 by no_of_ferries for more ferries
    for ferry_number in range(1, 17, 1):
        list_of_ferry['FERRY' + " " + str(ferry_number)] = ferry
    return list_of_ferry

# Returns the ferry schedule dictionary containing
# ferry number and schedule


def get_ferry_schedule():
    ferry_schedule = create_ferry_schedule(create_schedule_langkawi(create_timeslot()),
                                           create_schedule_penang(create_timeslot()))
    return ferry_schedule

# Returns ferry ID of the ferry associated with the
# customers choice of destination and time


def auto_select_ferry(destination_choice, time_choice):
    ferry_schedule = get_ferry_schedule()
    for ferry_id, schedule in ferry_schedule.items():
        destination = schedule[1]
        if destination_choice == destination:
            time_slot = schedule[2]
            for time in time_slot:
                if (time_choice == time):
                    return ferry_id


def get_source(destination_choice):
    ferry_schedule = get_ferry_schedule()
    for ferry_id, schedule in ferry_schedule.items():
        destination = schedule[1]
        if destination_choice == destination:
            return schedule[0]

# Returns whether ferry is full or not


def is_ferry_full(ferry_id, ferry_list):
    for ferry_number, ferry in ferry_list.items():
        if ferry_number == ferry_id:
            for seat_number, availability in ferry.items():
                if availability == 0:
                    return False
                elif availability == 1:
                    continue
            return True

# Returns if business/economy zone seats are available or not


def is_zone_available(ferry_id, type_of_seat, ferry_list):
    ferry = ferry_list[ferry_id]

    business = list(ferry)
    economy = list(ferry)
    if (type_of_seat == "BUSINESS"):
        business = business[:10]
        for seat in business:
            if ferry[seat] == 0:
                return True
        return False
    else:
        economy = economy[10:]
        for seat in economy:
            if ferry[seat] == 0:
                return True
        return False

# Returns if seat chosen by customer is available or not


def is_seat_available(ferry_id, customer_seat, ferry_list):
    for ferry_number, ferry in ferry_list.items():
        if ferry_number == ferry_id:
            for seat_number, availability in ferry.items():
                if seat_number == customer_seat and availability == 0:
                    return True
                elif seat_number == customer_seat and availability == 1:
                    return False
                else:
                    continue

# Returns seating arrangement


def display_ferry_seats(ferry_id, ferry_list):
    clear_screen()
    ferry = ferry_list[ferry_id]
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    count = 0  # used to format the output so that after every 5 seats there is a \n or line-break
    print("-" * 65 + "\n\t\t\tSEATING ARRANGEMENT\n" + "-" * 65 + "\n")
    print("Ferry ID: {} \t\t\t\t Date: {}".format(ferry_id, date))
    print(Fore.YELLOW, "\n" + "-" * 65
          + "\n\t\t\tBUSINESS CLASS\n" + "-" * 65, Fore.RESET)
    for seat_number, availability in ferry.items():
        count += 1
        if availability == 0:
            seat_color = Back.BLUE
        else:
            seat_color = Back.RED
        if count % 5 != 0:
            print(Back.RESET, " ", end=' ')
            print(seat_color, "* {} * ".format(seat_number, availability), end=' ')
        if count == 10:
            print(Back.RESET, " ", end=' ')
            print(seat_color, "* {} * ".format(seat_number, availability), end=' ')
            print(Back.RESET, Fore.CYAN, "\n" + "-" * 65 +
                  "\n\t\t\tECONOMY CLASS\n" + "-" * 65, Fore.RESET)
        elif count % 5 == 0:
            print(Back.RESET, " ", end=' ')
            print(seat_color, "* {} * ".format(seat_number, availability), end=' ')
            print("\n")
    print(Back.RESET, "\nB = Business Seats \t\t E = Economy Seats")
    print(Back.RED, "RED", end=' ')
    print(Back.RESET, "= Booked Seats\t\t", end=' ')
    print(Back.BLUE, "BLUE", end=' ')
    print(Back.RESET, "= Available Seats")
    input("Press [Enter] to continue. . .")

# Books an available seat and updates the dictionary and saves to file


def assign_seat(ferry_id, customer_seat, ferry_list):
    if is_ferry_full(ferry_id, ferry_list):
        print("The ferry is full next ferry is in one hour")
    else:
        if is_seat_available(ferry_id, customer_seat, ferry_list):
            for ferry_number, ferry in ferry_list.items():
                if ferry_number == ferry_id:
                    for seat_number, availability in ferry.items():
                        if seat_number == customer_seat:
                            ferry_list[ferry_id][customer_seat] = 1
                            save_to_file(ferry_list)
        else:
            return "Seat not available"


def print_purchasing_header():
    print("-" * 60, "\n\t\t\tPurchasing Module\n" + "-" * 60)


def prompt_user_seat(seat_type, seat_string, ferry_id, ferry_list):
    while (True):
        clear_screen()
        display_ferry_seats(ferry_id.upper(), ferry_list)
        seat_text = seat_string
        try:
            seat_number = input("\nType the seat number"
                        + seat_text + ": ")  # Add input validation
            seat_number = seat_number.upper()
            count = 0
            for ferry_number, ferry in ferry_list.items():
                if ferry_number == ferry_id:
                    for seat, availability in ferry.items():
                        count += 1
                        if seat_type == "BUSINESS" and count > 0 and count <= 10:
                            if seat == seat_number:
                                return seat_number
                        elif seat_type == "BUSINESS" and count > 10:
                            input("Please enter seats between [B01-B10]..Press [Enter] to Continue. .")
                            break
                        elif seat_type == "ECONOMY" and count > 10:
                            if seat == seat_number:
                                return seat_number
                        elif seat_type == "ECONOMY" and seat_number[0] == 'B' and count <= 10:
                            input("Please enter seats between [E01-E40]..Press [Enter] to Continue. .")
                            break
        except:
            input("Please input a valid seat number..Press [Enter] to Continue. .")


def get_type_of_seat():
    while (True):
        clear_screen()
        type_of_seat = input("""Select Type of Seat:

        B - Business
        E - Economy

Type the letter of the desired class of seat[Ex: B for Business] >> """)
        if type_of_seat.upper() == "B":
            return "business"
        elif type_of_seat.upper() == "E":
            return "economy"
        else:
            input(
                "Please enter only [B or E]. . Press [Enter] to try again. . . ")


def get_seat(type_of_seat, ferry_id, ferry_list):
    while (True):
        if type_of_seat == "BUSINESS":
            example_string = "[Ex: B04]"
        else:
            example_string = "[Ex: E06]"
        seat_number = prompt_user_seat(type_of_seat, example_string, ferry_id, ferry_list)
        seat_number = seat_number.upper()
        if (is_seat_available(ferry_id.upper(), seat_number, ferry_list)):
            assign_seat(ferry_id.upper(), seat_number, ferry_list)
            return seat_number
        else:
            input("Seat is not available please choose another seat!")

# Optimize this function


def purchase_menu():
    clear_screen()
    print_purchasing_header()
    ferry_list = file_exists()
    customer_name = get_name()
    destination_choice = get_destination()
    time_choice = get_time()
    ferry_schedule = get_ferry_schedule()
    ferry_id = auto_select_ferry(destination_choice, time_choice)
    if is_ferry_full(ferry_id, ferry_list):
        input(
            "Sorry the ferry is full, next ferry departs in 1 hour!\nPress [Enter] to Continue. . . ")
        main_menu()
    else:
        type_of_seat = get_type_of_seat()
        type_of_seat = type_of_seat.upper()
        if type_of_seat == "BUSINESS":
            if is_zone_available(ferry_id.upper(), type_of_seat, ferry_list):
                seat_number = get_seat(type_of_seat, ferry_id, ferry_list)
            else:
                type_of_seat = "ECONOMY"
                if is_zone_available(ferry_id.upper(), type_of_seat, ferry_list):
                    choice = input(
                        "Business zone is fully booked, is it okay to be placed in Economy Class? Type and Enter['Yes' or 'No'] >> ")
                    if choice.upper() == "YES":
                        seat_number = get_seat(
                            type_of_seat, ferry_id, ferry_list)
                    elif choice.upper() == "NO":
                        input(
                            "Next Ferry is in 1 hour\nPress [Enter] to Continue. . . ")
                        main_menu()
                    else:
                        input("Invalid input...Press [Enter] to try again. .")
                        seat_number = get_seat(
                            type_of_seat, ferry_id, ferry_list)
                else:
                    input(
                        "Ferry is full, next ferry is in 1 hour\nPress [Enter] to Continue. . . ")
                    main_menu()
        else:
            if is_zone_available(ferry_id.upper(), type_of_seat, ferry_list):
                seat_number = get_seat(type_of_seat, ferry_id, ferry_list)
            else:
                type_of_seat = "BUSINESS"
                if is_zone_available(ferry_id.upper(), type_of_seat, ferry_list):
                    choice = input(
                        "Economy zone is fully booked, is it okay to be placed in Business Class? ['Yes' or 'No'] ")
                    if choice.upper() == "YES":
                        seat_number = get_seat(
                            type_of_seat, ferry_id, ferry_list)
                    elif choice.upper() == "NO":
                        input(
                            "Next Ferry is in 1 hour\nPress [Enter] to Continue. . . ")
                        main_menu()
                    else:
                        input("Invalid input... Press [Enter] to try again. .")
                        seat_number = get_seat(
                            type_of_seat, ferry_id, ferry_list)
                else:
                    input(
                        "Ferry is full, next ferry is in 1 hour\nPress [Enter] to Continue. . . ")
                    main_menu()
    source = get_source(destination_choice)
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    time_choice = str(time_choice) + ":00"
    print_boarding_ticket(customer_name, source, destination_choice,
                          date, time_choice, type_of_seat, seat_number, ferry_id)


def view_seating():
    while (True):
        clear_screen()
        selection = input("-" * 60 + "\n\t\t\tSEATING ARRANGEMENT MODULE\n" + "-" * 60 + """

        F - To select Ferry ID
        M - Return to Main Menu

Please enter one of the Options[F or M]: """)
        if (selection.upper() == "F"):
            ferry_menu()
        #elif (selection.upper() == "T"):
            #trip_time_menu()  # Need to make menu
        elif (selection.upper() == "M"):
            main_menu()
        else:
            input(
                "Invalid Input! Please try again... Press [Enter] to Continue. . . ")


def ferry_selection(ferry_list):
    while (True):
        clear_screen()
        try:
            print("\nSELECT A FERRY TO VIEW THE SEATING ARRANGEMENT\n\n")
            for number, ferry_number in enumerate(ferry_list):
                print(number + 1, "-->", ferry_number)
            print("\n")
            selection = int(
                input("Enter the number to view the associated ferry seating [Ex: 2] >> "))
            if (selection > 0 and selection < 17):
                return selection
            else:
                input(
                    "Please enter number between 1 and 16.. Press [Enter] to Continue. .")
        except ValueError:
            input("Please enter numbers only! Press [Enter] to continue. .")


def chosen_ferry(selection, ferry_list):
    for number, ferry_number in enumerate(ferry_list):
        if (selection == number):
            return ferry_number
        else:
            continue


# Improve this function
def ferry_menu():
    ferry_list = file_exists()
    while (True):
        clear_screen()
        selection = ferry_selection(ferry_list)
        ferry_id = chosen_ferry(selection - 1, ferry_list)
        if ferry_id.upper() in ferry_list:
            display_ferry_seats(ferry_id.upper(), ferry_list)
            break
        else:
            input("Enter valid ferry number! Press [Enter] to try again. .")


def main_menu():
    while (True):
        clear_screen()
        selection = input("-" * 60 + "\n\t\t\tMain Menu\n" + "-" * 60 + """

        P - To Purchase Ticket
        V - To View Seating Arrangement
        Q - To Quit the System

Please Enter one of the Options[P or V or Q]: """)
        if (selection.upper() == "P"):
            purchase_menu()
        elif (selection.upper() == "V"):
            view_seating()
        elif (selection.upper() == "Q"):
            while True:
                choice = input(
                    "Are you sure you want to quit?(Y - Yes or N - No) >> ")
                if choice.upper() == 'Y':
                    quit()
                elif choice.upper() == "N":
                    main_menu()
                else:
                    input("Please answer with Y or N.. ")
                    clear_screen()
        else:
            input(
                "\nInvalid Input!\nPlease try again...Press [Enter] to Continue. . . ")

# Checks whether ferryseats.json file exists which
# is the File used to save data of seating arrangement
# If it doesn't exists a new file is created with
# All seats initially unbooked


def file_exists():
    if data_path_exists():
        try:
            with open('data/ferryseats.json') as seats_data:
                ferry_list = json.load(seats_data)
            return ferry_list
        except FileNotFoundError:
            with open('data/ferryseats.json', 'w') as file:
                json.dump(create_ferry_list(init_ferry()), file)
        finally:
            with open('data/ferryseats.json') as seats_data:
                ferry_list = json.load(seats_data)
            return ferry_list

# Checks Whether Folder 'data' exists
# If it doesn't creates the folder


def data_path_exists():
    if os.path.exists('data'):
        return True
    else:
        os.mkdir('data')
        return True


def save_to_file(ferry_list):
    with open('data/ferryseats.json', 'w') as file:
        json.dump(ferry_list, file)


def read_from_file():
    with open('data/ferryseats.json') as seats_data:
        ferry_list = json.load(seats_data)
    return ferry_list


def print_boarding_ticket(customer_name, source, destination, date, time, type_of_seat, seat_number, ferry_number):
    clear_screen()
    print("-" * 60 + "\n\t\t\tBOARDING TICKET\n" + "-" * 60)
    print("Customer Name: {}\nSource: {}\t\t\tDestination: {}\nDate: {}\t\t\tTime: {}\nType Of Seat: {}\t\t\tSeat Number: {}\nFerry ID: {}".format(customer_name, source,
                                                                                                                                                     destination, date, time,
                                                                                                                                                     type_of_seat, seat_number,
                                                                                                                                                     ferry_number))
    print("-" * 60 + "\n")
    input("Press [Enter] key to return to main menu. . . ")


main_menu()

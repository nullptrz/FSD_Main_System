import json
import os
from colorama import Fore, Back, Style
from colorama import init

# intialize the colorama module
init()


# To create a ferry with N business and M economy Seats

def init_ferry():
    ferry = {}
    for x in range(1, 11, 1):
        if x >= 10:
            x = 'B' + str(x)
        else:
            x = 'B0' + str(x)
        ferry[x] = 0
    for x in range(1, 41, 1):
        if x < 10:
            x = 'E0' + str(x)
        else :
            x = 'E' + str(x)
        ferry[x] = 0
    return ferry

def add_ferry(ferry):
    list_of_ferry = {}
    for a in range(1, 9, 1):
        list_of_ferry['FERRY' + " " +str(a)] = ferry
    return list_of_ferry

def print_ferry_seats(user_input, list_of_ferries):
            count = 0
            for key, value in list_of_ferries.items():
                if key == user_input:
                    for seat, num in value.items():
                        count += 1
                        if num == 0:
                            x = Back.BLUE
                        else:
                            x = Back.RED
                        if count % 5 != 0:
                                print(Back.RESET, " ", end=' ')
                                print(x,"* {} * ".format(seat, num), end=' ')
                        elif count % 5 == 0:
                                print(Back.RESET, " ", end=' ')
                                print(x, "* {} * ".format(seat, num), end=' ')
                                print("\n")
            print(Back.RED, "RED", end=' ')
            print(Back.RESET, "= Booked Seats\t\t", end=' ')
            print(Back.BLUE, "BLUE", end=' ' )
            print(Back.RESET,"= Available Seats")


def is_ferry_full(list_of_ferries, user_input):
    for key, value in list_of_ferries.items():
        if key == user_input:
            for seat, num in value.items():
                if num == 0:
                    return "Ferry not Full"
                elif num == 1:
                    continue
            return "Ferry is Full"

def is_seat_available(ferry, user_input, seat_number):
    for key, value in list_of_ferries.items():
        if key == user_input:
            for seat, num in value.items():
                if seat == seat_number and num == 0:     
                    return "Seat is available"
                elif seat == seat_number and num == 1:
                    return "Seat not Available"
                else:
                    continue
                
                    


def data_path_exists():
    if os.path.exists('data'):
        return True
    else:
        os.mkdir('data')
        return True

def file_exists():
    if data_path_exists():
        try:
            with open('data/ferryseats.json') as seats_data:
                list_of_ferries = json.load(seats_data)
            return list_of_ferries
        except:
            with open('data/ferryseats.json', 'w') as file:
                json.dump(add_ferry(init_ferry()), file)
        finally:
            with open('data/ferryseats.json') as seats_data:
                list_of_ferries = json.load(seats_data)
            return list_of_ferries
                    
            

user_input = input("Enter Ferry: \n>> ")
list_of_ferries = file_exists()
print_ferry_seats(user_input.upper(), list_of_ferries)
seat_number = input("Enter Seat Number: \n>> ")
print(is_seat_available(list_of_ferries, user_input.upper(), seat_number.upper()))
input()








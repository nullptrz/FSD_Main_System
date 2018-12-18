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




try:
    if os.path.exists('data'):
        with open('data/ferryseats.json') as seatdata:
            list_of_ferries=json.load(seatdata)
    elif not os.path.exists('data'):
        os.mkdir('data')
        with open('data/ferryseats.json', 'w') as file:
          json.dump(add_ferry(init_ferry()), file)
except:
    with open('data/ferryseats.json', 'w') as file:
          json.dump(add_ferry(init_ferry()), file)
finally:
    with open('data/ferryseats.json') as seatdata:
        list_of_ferries=json.load(seatdata)
    user_input = input("Enter ferry: ")
    print_ferry_seats(user_input.upper(), list_of_ferries)
    input("Hello what is your name: ")





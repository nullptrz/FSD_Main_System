"""
Created on Wednesday 19th December 2018
@author: ALI AHSAN SAEED
"""


import json
import os
from colorama import Fore, Back, Style
from colorama import init


# intialize the colorama module

init()

# To create a ferry with N business and M economy Seats #
# But it is assumed that the ferries have 10 Business and 40 Economy Seats #
# Also if a file containing data does not exist this function helps to create it #


def init_ferry():
    ferry = {}
    for x in range(1, 11, 1): # Could replace 11 by N to accomodate more seats
        if x >= 10:
            x = 'B' + str(x)
        else:
            x = 'B0' + str(x)
        ferry[x] = 0
    for x in range(1, 41, 1): # Could replace 40 by M to accomodate more seats
        if x < 10:
            x = 'E0' + str(x)
        else :
            x = 'E' + str(x)
        ferry[x] = 0
    return ferry

# Adds 8 Ferries to another dictionary/ Used to create a list of ferries #


def add_ferry(ferry):
    list_of_ferry = {}
    for a in range(1, 9, 1): # Could replace 9 by no_of_ferries for more ferries
        list_of_ferry['FERRY' + " " +str(a)] = ferry
    return list_of_ferry

#  To print all the seats of a specific ferry that the user enters # 


def print_ferry_seats(customer_ferry, list_of_ferries):
            count = 0
            for ferry_number, ferry in list_of_ferries.items():
                if ferry_number == customer_ferry:
                    for seat_number, availability in ferry.items():
                        count += 1
                        if availability == 0:
                            x = Back.BLUE
                        else:
                            x = Back.RED
                        if count % 5 != 0:
                                print(Back.RESET, " ", end=' ')
                                print(x,"* {} * ".format(seat_number, availability), end=' ')
                        elif count % 5 == 0:
                                print(Back.RESET, " ", end=' ')
                                print(x, "* {} * ".format(seat_number, availability), end=' ')
                                print("\n")
            print(Back.RED, "RED", end=' ')
            print(Back.RESET, "= Booked Seats\t\t", end=' ')
            print(Back.BLUE, "BLUE", end=' ' )
            print(Back.RESET,"= Available Seats")


def is_ferry_full(customer_ferry, list_of_ferries):
    for ferry_number, ferry in list_of_ferries.items():
        if ferry_number == customer_ferry:
            for seat_number, availability in ferry.items():
                if availability == 0:
                    return False
                elif availability == 1:
                    continue
            return True


def is_seat_available(customer_ferry, customer_seat, list_of_ferries):
    for ferry_number, ferry in list_of_ferries.items():
        if ferry_number == customer_ferry:
            for seat_number, availability in ferry.items():
                if seat_number == customer_seat and availability == 0:
                    return "Seat is available"
                elif seat_number == customer_seat and availability == 1:
                    return "Seat not Available"
                else:
                    continue


def assign_seat(customer_ferry, customer_seat, list_of_ferries):
    if is_ferry_full(customer_ferry, list_of_ferries):
        print("The ferry is full next ferry is in one hour")
    else:
        if is_seat_available(customer_ferry, customer_seat, list_of_ferries):
            for ferry_number, ferry in list_of_ferries.items():
                if ferry_number == customer_ferry:
                    for seat_number, availability in ferry.items():
                        if seat_number == customer_seat:
                            list_of_ferries[customer_ferry][customer_seat] = 1
                            save_to_file(list_of_ferries)
        else:
            print("The seat is not available")

# Checks if the directory/folder named path exists
# if it doesn't then creates one

def data_path_exists():
    if os.path.exists('data'):
        return True
    else:
        os.mkdir('data')
        return True

# Checks if the file ferryseats.json exists which is the file
# That contains all data if it doesn't then it calls functions
# init_ferry to initialize ferry dictionary and then add_ferry
# To create a list of ferries and saves it as ferryseats.

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


def save_to_file(list_of_ferries):
    with open('data/ferryseats.json', 'w') as file:
        json.dump(list_of_ferries, file)


def read_from_file():
    with open('data/ferryseats.json') as seats_data:
              list_of_ferries = json.load(seats_data)
    return list_of_ferries

user_input = input("Enter Ferry: \n>> ")
list_of_ferries = file_exists()
print_ferry_seats(user_input.upper(), list_of_ferries)
seat_number = input("Enter Seat Number: \n>> ")
print(is_seat_available(user_input.upper(), seat_number.upper(), list_of_ferries))
assign_seat(user_input.upper(), seat_number.upper(), list_of_ferries)
print_ferry_seats(user_input.upper(), read_from_file())
input()

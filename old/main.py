"""
Created on Wednesday 19th December 2018
@author: ALI AHSAN SAEED

PROGRAM: Ferry Ticketing System
         System to view and assign
         Seats for customers.
"""


import json
import os
from colorama import Fore, Back, Style
from colorama import init


# initialize the colorama module

init()

# To create a ferry with N business and M economy Seats #
# But it is assumed that the ferries have 10 Business and 40 Economy Seats #


def init_ferry():
    ferry = {}
    for business_seats in range(1, 11, 1):  # Could replace 11 by N to accommodate more seats
        if business_seats >= 10:
            business_seats = 'B' + str(business_seats)
        else:
            business_seats = 'B0' + str(business_seats)
        ferry[business_seats] = 0
    for economy_seats in range(1, 41, 1):  # Could replace 40 by M to accommodate more seats
        if economy_seats < 10:
            economy_seats = 'E0' + str(economy_seats)
        else:
            economy_seats = 'E' + str(economy_seats)
        ferry[economy_seats] = 0
    return ferry

# Adds 8 Ferries to another dictionary/ Used to initially create a list of ferries #
# Uses the ferries created by the init_ferry function #


def create_ferry_list(ferry):
    list_of_ferry = {}
    for a in range(1, 9, 1):  # Could replace 9 by no_of_ferries for more ferries
        list_of_ferry['FERRY' + " " + str(a)] = ferry
    return list_of_ferry

#  To print all the seats of a specific ferry that the user enters #


def print_ferry_seats(customer_ferry, list_of_ferries):
            count = 0 #used to format the output so that after every 5 seats there is a \n or line-break
            count_of_ferries = 0
            for ferry_number, ferry in list_of_ferries.items():
                count_of_ferries += 1
                if ferry_number == customer_ferry:
                    for seat_number, availability in ferry.items():
                        count += 1
                        if availability == 0:
                            seat_color = Back.BLUE
                        else:
                            seat_color = Back.RED
                        if count % 5 != 0:
                                print(Back.RESET, " ", end=' ')
                                print(seat_color, "* {} * ".format(seat_number, availability), end=' ')
                        elif count % 5 == 0:
                                print(Back.RESET, " ", end=' ')
                                print(seat_color, "* {} * ".format(seat_number, availability), end=' ')
                                print("\n")
                elif count_of_ferries == len(list_of_ferries):
                    print("Enter valid ferry number")
                else:
                    continue
            print(Back.RED, "RED", end=' ')
            print(Back.RESET, "= Booked Seats\t\t", end=' ')
            print(Back.BLUE, "BLUE", end=' ')
            print(Back.RESET, "= Available Seats")


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

# Checks if the directory/folder named 'data' exists #
# if it doesn't then creates one #


def data_path_exists():
    if os.path.exists('data'):
        return True
    else:
        os.mkdir('data')
        return True

# Checks if the file ferryseats.json exists which is the file #
# That contains all data if it doesn't then it calls functions #
# init_ferry to initialize ferry dictionary and then create_ferry_list #
# To create a list of ferries and saves it as ferryseats. #


def file_exists():
    if data_path_exists():
        try:
            with open('data/ferryseats.json') as seats_data:
                list_of_ferries = json.load(seats_data)
            return list_of_ferries
        except FileNotFoundError:
            with open('data/ferryseats.json', 'w') as file:
                json.dump(create_ferry_list(init_ferry()), file)
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


ferry_choice = input("Enter Ferry: \n>> ")
ferry_list = file_exists()
print_ferry_seats(ferry_choice.upper(), ferry_list)
seat_choice = input("Enter Seat Number: \n>> ")
print(is_seat_available(ferry_choice.upper(), seat_choice.upper(), ferry_list))
assign_seat(ferry_choice.upper(), seat_choice.upper(), ferry_list)
print_ferry_seats(ferry_choice.upper(), read_from_file())
input("Test: ")

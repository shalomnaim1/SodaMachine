from typing import List, Tuple
from enum import Enum


class DEAL_STATUS(Enum):
    APPROVED = 0
    INVALID_CARD_NUMBER = 1
    NO_BALANCE = 3
    FAIL_TO_WITHDRAW = 4
    UNKNOWN = 5


class VisaApi:

    @staticmethod
    def is_valid_card(visa_server_address, username, password, credit_card_number):
        return DEAL_STATUS.INVALID_CARD_NUMBER

    @staticmethod
    def is_balance_available(visa_server_address, username, password, credit_card_number, amount):
        return DEAL_STATUS.NO_BALANCE

    @staticmethod
    def withdraw_money(visa_server_address, username, password, credit_card_number, amount):
        return DEAL_STATUS.FAIL_TO_WITHDRAW


class VisaClient:
    def __init__(self, visa_server_address, username, password):
        self.visa_server_address = visa_server_address
        self.username = username
        self.password = password

    @classmethod
    def create(cls, visa_server_address, username, password):
        return cls(visa_server_address, username, password)

    def make_a_deal(self, credit_card_number, amount):
        deal_status = DEAL_STATUS.UNKNOWN

        deal_status = VisaApi.is_valid_card(self.visa_server_address, self.username, self.password,
                                            credit_card_number)

        if deal_status != DEAL_STATUS.APPROVED:
            return deal_status

        deal_status = VisaApi.is_balance_available(self.visa_server_address, self.username,
                                                   self.password, credit_card_number, amount)
        if deal_status != DEAL_STATUS.APPROVED:
            return deal_status

        deal_status = VisaApi.withdraw_money(self.visa_server_address, self.username,
                                             self.password, credit_card_number, amount)

        return deal_status


class Drink:
    def __init__(self, amount, price):
        self.amount = amount
        self.price = price

    def get_one(self):
        self.amount -= 1

        if self.amount < 1:
            print("Can't get a drink")
            return False

        return True

    def load_more(self, amount):
        if amount < 0:
            print("Can't load negative amount of cans")
            return False
        else:
            self.amount += amount
            return True

    def __repr__(self):
        return f"amount: {self.amount}, price: {self.price}"


class SodaMachine:
    def __init__(self, drinks_mapping, visa_client):
        self.drinks = {}

        for drink_name, drink_object in drinks_mapping.items():
            self.drinks[drink_name] = drink_object

        self.visa_client = visa_client

    def add_new_kind_of_drink(self, drink_name, amount_of_cans, can_price):

        if amount_of_cans >= 0 and can_price >= 0:
            self.drinks[drink_name] = Drink(amount_of_cans, can_price)
        else:
            raise Exception(
                f"Invalid param supplied to start, {(drink_name, amount_of_cans, can_price)}, "
                f"fail to start machine")

    @classmethod
    def start(cls, drinks_mapping: List[Tuple[str, int, int]], visa_server, username, password):

        visa_client = VisaClient.create(visa_server, username, password)

        instance = cls({}, visa_client)

        for drink_name, amount_of_cans, can_price in drinks_mapping:
            instance.add_new_kind_of_drink(drink_name, amount_of_cans, can_price)

        return instance

    def load_drink_to_machine(self, drink_name, amount, price=None):
        if drink_name in self.drinks:
            self.drinks[drink_name].load_more(amount)
        elif price is not None:
            self.add_new_kind_of_drink(drink_name, amount, price)
        print(self.drinks)

    def buy_a_drink(self, name, payment_method, cash_amount=None, credit_card_number=None):
        if name in self.drinks:
            if payment_method == "cash" and cash_amount >= self.drinks[name].price:
                self.drinks[name].get_one()
                print(f"enjoy your {name} can, your change is {cash_amount - self.drinks[name].price}")
                return True
            elif payment_method == "credit-card":
                deal_status = self.visa_client.make_a_deal(credit_card_number, self.drinks[name].price)
                if deal_status == DEAL_STATUS.APPROVED:
                    self.drinks[name].get_one()
                    print(
                        f"enjoy your {name} can, your card with number {credit_card_number} "
                        f"charged with {self.drinks[name].price} NIS")
                else:
                    print(f"sorry, something when wrong, you cant have your soda,"
                          f" error {deal_status.name}")
                return deal_status

        else:
            print("sorry, something when wrong, you cant have your soda")
            return False

    def __str__(self):
        return "\n".join(f"drink_name: {self.drinks[drink_name]}" for drink_name in self.drinks)


def main():
    my_machine = SodaMachine.start([("Coke", 10, 10), ("Orange Juice", 10,15), ("Water", 10, 7)],
                                   "server_address", "username", "password")


    while True:
        print("Soda Machine:")
        print("1. Buy a soda")
        print("2. Load more soda cans")
        print("3. Exit")
        pick_action = input("Pick action: ")

        if pick_action == "1":
            print("Name, Price")

            for drink_name in my_machine.drinks:
                print(f"{drink_name}, {my_machine.drinks[drink_name].price}")

            drink_name = input(f"What soda do you wanna have? ")

            print("1. Cash")
            print("2. Credit card")
            payment_method = input("Pick payment method: ")

            if payment_method == "1":
                cash_amount = input(f"Enter amount of coins? ")
                my_machine.buy_a_drink(drink_name, "cash", cash_amount=int(cash_amount))
            elif payment_method == "2":
                card_number = input("Enter credit card number: ")
                my_machine.buy_a_drink(drink_name, "credit-card", credit_card_number=card_number)
            else:
                print("Invalid choose please try again...")
        elif pick_action == "2":
            drink_name = input("What drink you want to load? ")
            drink_amount = input("How many cans you have? ")

            if drink_name not in my_machine.drinks:
                price = input("This is a new produce, please enter price? ")
                my_machine.load_drink_to_machine(drink_name, drink_amount, price)
            else:
                my_machine.load_drink_to_machine(drink_name, drink_amount)
        elif pick_action == "3":
            print("ByeBye, see ya next time")
            break
        else:
            print("Invalid choose please try again...")
        print("\n\n")


if __name__ == "__main__":
    main()

from typing import List, Tuple


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
    def __init__(self, drinks_mapping):
        self.drinks = {}

        for drink_name, drink_object in drinks_mapping.items():
            self.drinks[drink_name] = drink_object

    def add_new_kind_of_drink(self, drink_name, amount_of_cans, can_price):

        if amount_of_cans >= 0 and can_price >= 0:
            self.drinks[drink_name] = Drink(amount_of_cans, can_price)
        else:
            raise Exception(
                f"Invalid param supplied to start, {(drink_name, amount_of_cans, can_price)}, "
                f"fail to start machine")

    @classmethod
    def start(cls, drinks_mapping: List[Tuple[str, int, int]]):
        instance = cls({})

        for drink_name, amount_of_cans, can_price in drinks_mapping:
            instance.add_new_kind_of_drink(drink_name, amount_of_cans, can_price)

        return instance

    def load_drink_to_machine(self, drink_name, amount, price=None):
        if drink_name in self.drinks:
            self.drinks[drink_name].load_more(amount)
        elif price is not None:
            self.add_new_kind_of_drink(drink_name, amount, price)
        print(self.drinks)

    def buy_a_drink(self, name, cash_amount):
        if name in self.drinks and cash_amount >= self.drinks[name].price:
            self.drinks[name].get_one()
            print(f"enjoy your {name} can, your change is {cash_amount - self.drinks[name].price}")
            return True
        else:
            print("sorry, something when wrong, you cant have your soda")
            return False

    def __str__(self):
        return "\n".join(f"drink_name: {self.drinks[drink_name]}" for drink_name in self.drinks)


def main():
    my_machine = SodaMachine.start([("Coke", 10, 10), ("Orange Juice", 10, 15), ("Water", 10, 7)])

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

            cash_amount = input(f"Enter amount of coins? ")
            my_machine.buy_a_drink(drink_name, int(cash_amount))
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


if __name__ == "__main__":
    main()

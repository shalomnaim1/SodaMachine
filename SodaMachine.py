from typing import List, Tuple


class Visa:
    def withdraw(self, card_id, amount):
        raise Exception("kokoko")


class Drink:
    def __init__(self, name, amount, price):
        self.name = name
        self.amount = amount
        self.price = price

    def get_one(self):
        self.amount -= 1
        return True

    def load_more(self, amount):
        self.amount = amount


class SodaMachine:
    def __init__(self, drinks_mapping):
        self.drinks_mapping = drinks_mapping
        self.visa = Visa()

    @classmethod
    def start(cls, drinks_mapping: List[Tuple[str, int, int]]):
        for drink_name, amount, price in drinks_mapping:
            if amount < 0:
                raise Exception(f"Invalid amount of {drink_name}")

        mapping = {drink_name: Drink(drink_name, amount, price)
                   for drink_name, amount, price in drinks_mapping}
        
        return cls(mapping)

    def load_drinks(self, drink_name, amount):
        self.drinks_mapping[drink_name] = amount

    def buy_a_drink(self, name, currency=None, credit_card=None):
        if credit_card:
            if self.visa.withdraw(credit_card, self.drinks_mapping[name].price):
                return name, 0
        else:
            if currency >= self.drinks_mapping[name].price and self.drinks_mapping[name].amount > 0:
                self.drinks_mapping[name].get_one()
                return name, currency - self.drinks_mapping[name].price

        return None, None


# def __init__(self, drinks_mapping)
# make sure that all attr init with right values

# def start(cls, drinks_mapping: List[Tuple[str, int, int]])
# invalid price, negative
# invalid amount, negative
# validate price
# validate amount

# def load_drinks(self, drink_name, amount)
# invalid amount, negative
# validate amount

# def buy_a_drink(self, name, currency)
# get a soda
# ge a soda, negative currency

import pytest
from unittest.mock import MagicMock, patch

from SodaMachine import SodaMachine, Drink


class MockVisa:
    def __init__(self):
        self.allow_deal = None

    def withdraw(self, card_id, amount):
        if self.allow_deal is None:
            raise Exception("Visa response wasn't configured")

        return bool(self.allow_deal)

    def set_no_balance(self):
        self.allow_deal = False

    def set_allow_transaction(self):
        self.allow_deal = True


@pytest.fixture
def coke_drink():
    instance = Drink(name="Coke", amount=10, price=7)
    yield instance
    print("Kuku")


@pytest.fixture
def orange_drink():
    return Drink(name="Orange", amount=5, price=10)


@pytest.fixture
def soda_machine(coke_drink, orange_drink):
    return SodaMachine({"Coke": coke_drink, "Orange": orange_drink})


@pytest.fixture
def blocked_credit_card_soda_machine(coke_drink, orange_drink):
    with patch("SodaMachine.Visa", MockVisa):
        instance = SodaMachine({"Coke": coke_drink, "Orange": orange_drink})
        instance.visa.set_allow_transaction()
        return instance


def test_create_soda_machine():
    my_input = "my_input"

    instance = SodaMachine(my_input)

    assert instance.drinks_mapping == "my_input"


@pytest.mark.parametrize("currency, expected_currency_result, expected_soda_result",
                         [(10, 3, "Coke"), (-10, None, None)])
def test_order_a_drink(soda_machine, currency, expected_currency_result, expected_soda_result):
    drink, change = soda_machine.buy_a_drink("Coke", currency)

    assert drink == expected_soda_result, "wrong drink returned"
    assert change == expected_currency_result, "wrong change returned"


def test_order_using_credit_card(blocked_credit_card_soda_machine):

    drink, change = blocked_credit_card_soda_machine.buy_a_drink("Coke", credit_card=123)

    assert drink == "Coke", "wrong drink returned"
    assert change == 0, "wrong change returned"

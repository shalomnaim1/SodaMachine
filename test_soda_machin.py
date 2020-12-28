import pytest
from SodaMachine import SodaMachine


@pytest.fixture
def soda_machine():
    return SodaMachine.start([("Coke", 10, 10)])


def test_create_soda_machine():
    machine = SodaMachine.start([("Coke", 10, 10)])
    assert "Coke" in machine.drinks, "Coke is missing in machine"
    assert machine.drinks["Coke"].price == 10, "Wrong price was set to Coke"
    assert machine.drinks["Coke"].amount == 10, "Wrong amount was set to Coke"


@pytest.mark.parametrize("drink_name, amount, price", [("Cֹoke", 10, -5), ("Cֹoke", -10, 5)])
def test_create_soda_machine_with_invalid_params(drink_name, amount, price):
    with pytest.raises(Exception):
        SodaMachine.start([(drink_name, amount, price)])


@pytest.mark.parametrize("drink_name, amount, price, new_amount", [("Coke", 10, 10, 20),
                                                                   ("Water", 10, 5, 10)])
def test_load_drinks(soda_machine, drink_name, amount, price, new_amount):
    soda_machine.load_drink_to_machine(drink_name, amount, price)

    assert drink_name in soda_machine.drinks, f"{drink_name} isn't loaded in the machine"
    assert soda_machine.drinks[drink_name].amount == new_amount, "wrong amount found in the machine"

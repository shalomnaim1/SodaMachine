from soda_machine import DEAL_STATUS
import pytest
from soda_machine import SodaMachine
from unittest.mock import patch


class MockedVisaApi:
    IS_VALID_CARD = True
    IS_BALANCE_AVAILABLE = True
    WITHDRAW_MONEY = True

    @staticmethod
    def is_valid_card(visa_server_address, username, password, credit_card_number):
        if MockedVisaApi.IS_VALID_CARD:
            return DEAL_STATUS.APPROVED
        return DEAL_STATUS.INVALID_CARD_NUMBER

    @staticmethod
    def is_balance_available(visa_server_address, username, password, credit_card_number, amount):
        if MockedVisaApi.IS_BALANCE_AVAILABLE:
            return DEAL_STATUS.APPROVED
        return DEAL_STATUS.NO_BALANCE

    @staticmethod
    def withdraw_money(visa_server_address, username, password, credit_card_number, amount):
        if MockedVisaApi.WITHDRAW_MONEY:
            return DEAL_STATUS.APPROVED
        return DEAL_STATUS.FAIL_TO_WITHDRAW


@pytest.fixture
def soda_machine():
    return SodaMachine.start([("Coke", 10, 10)], "visa_server", "username", "password")


@patch("soda_machine.VisaApi", MockedVisaApi)
def test_buy_drink_using_credit_card(soda_machine):
    is_success = soda_machine.buy_a_drink("Coke", "credit-card", credit_card_number=1234)
    assert is_success, "fail to buy a drink using a credit card"


@patch("soda_machine.VisaApi", MockedVisaApi)
def test_failed_credit_card_validation(soda_machine):
    MockedVisaApi.IS_VALID_CARD = False
    is_success = soda_machine.buy_a_drink("Coke", "credit-card", credit_card_number=1234)
    assert is_success == DEAL_STATUS.INVALID_CARD_NUMBER, "expected to fail"



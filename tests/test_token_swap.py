from unicodedata import decimal
import brownie
from brownie import accounts, BasicToken, TokenSwap
from web3 import Web3
import pytest


@pytest.fixture
def beer(accounts):
    return BasicToken.deploy("Beer Token", "BEER", 18, {"from": accounts[0]})


@pytest.fixture
def coffee(accounts):
    return BasicToken.deploy("Coffee Token", "COFF", 18, {"from": accounts[0]})


@pytest.fixture
def house(accounts):
    return BasicToken.deploy("House Token", "HOUS", 2, {"from": accounts[0]})


@pytest.fixture
def car(accounts):
    return BasicToken.deploy("Car Token", "CAR", 5, {"from": accounts[0]})


def setup_swap(beer, coffee, beer_ratio, coffee_ratio):
    swap = TokenSwap.deploy(
        beer.address, coffee.address, beer_ratio, coffee_ratio, {"from": accounts[0]}
    )
    user = accounts[1]
    tx = beer.faucet({"from": swap.address})
    tx = beer.faucet({"from": user})
    tx = coffee.faucet({"from": swap.address})
    tx.wait(1)
    return swap, user


def test_deploy_token_swap(beer, coffee):
    swap, _ = setup_swap(beer, coffee, 1, 1)
    assert beer.balanceOf(swap.address) == 100000
    assert coffee.balanceOf(swap.address) == 100000


def test_swap(beer, coffee):
    swap, user = setup_swap(beer, coffee, 1, 1)
    tx = beer.approve(swap.address, 10, {"from": user})
    tx.wait(1)
    tx = swap.swapAforB(10, {"from": user})
    tx.wait(1)
    assert beer.balanceOf(user) == 99990
    assert coffee.balanceOf(user) == 10


def test_unbalanced_swap(beer, coffee):
    swap, user = setup_swap(beer, coffee, 2, 1)
    tx = beer.approve(swap.address, 10, {"from": user})
    tx.wait(1)
    tx = swap.swapAforB(10, {"from": user})
    tx.wait(1)
    assert beer.balanceOf(user) == 99990
    assert coffee.balanceOf(user) == 5


def test_non_integer_swap(beer, coffee):
    swap, user = setup_swap(beer, coffee, 3, 2)
    tx = beer.approve(swap.address, 10, {"from": user})
    tx.wait(1)
    tx = swap.swapAforB(10, {"from": user})
    tx.wait(1)
    assert beer.balanceOf(user) == 99991
    assert coffee.balanceOf(user) == 6


def test_decimal_swap(house, car):
    """Handling of decimals should be done off-chain, not on-chain.
    With the current setup that is easy, the ratio values just need to be
    adjusted to match the decimal values of the tokens.
    Assume a House token with 2 decimal places, and a car token with 5 decimal places.
    Also assume that the ratio is 3:20 (3 House tokens for every 20 car tokens).

    The contracts internal representation needs to be 300000:2000 (3 * 10 ** 5 : 20 * 10 ** 2).

    """
    swap, user = setup_swap(
        house, car, 3 * 10 ** car.decimals(), 20 * 10 ** house.decimals()
    )
    tx = house.approve(swap.address, 3000, {"from": user})
    tx.wait(1)
    tx = swap.swapAforB(3000, {"from": user})
    tx.wait(1)
    assert house.balanceOf(user) == 97000
    assert car.balanceOf(user) == 20
    with brownie.reverts():
        tx = swap.swapAforB(2, {"from": user})
        tx.wait(1)


def test_cannot_swap_without_allowance(beer, coffee):
    swap, user = setup_swap(beer, coffee, 1, 1)
    tx = beer.approve(swap.address, 0, {"from": user})
    tx.wait(1)
    with brownie.reverts():
        tx = swap.swapAforB(10, {"from": user})
        tx.wait(1)

import brownie
from brownie import accounts, BeerToken, CoffeeToken, TokenSwap
from web3 import Web3
import pytest


@pytest.fixture
def beer(BeerToken, accounts):
    return BeerToken.deploy({"from": accounts[0]})


@pytest.fixture
def coffee(CoffeeToken, accounts):
    return CoffeeToken.deploy({"from": accounts[0]})


@pytest.fixture
def swap(beer, coffee, accounts):
    return TokenSwap.deploy(beer.address, coffee.address, 1, 1, {"from": accounts[0]})


@pytest.fixture
def decimal_swap(beer, coffee, accounts):
    return TokenSwap.deploy(beer.address, coffee.address, 3, 2, {"from": accounts[0]})


@pytest.fixture
def unbalanced_swap(beer, coffee, accounts):
    # 2 beer tokens are worth 1 coffee token
    return TokenSwap.deploy(beer.address, coffee.address, 2, 1, {"from": accounts[0]})


def test_deploy_token_swap(beer, coffee, swap):
    tx = beer.getBeer({"from": swap.address})
    tx.wait(1)
    assert beer.balanceOf(swap.address) == 100
    tx = coffee.getCoffee({"from": swap.address})
    tx.wait(1)
    assert coffee.balanceOf(swap.address) == 100


def test_swap(beer, coffee, swap):
    user = accounts[1]
    tx = beer.getBeer({"from": swap.address})
    tx = beer.getBeer({"from": user})
    tx = coffee.getCoffee({"from": swap.address})
    tx.wait(1)
    tx = beer.approve(swap.address, 10, {"from": user})
    tx.wait(1)
    tx = swap.swapAforB(10, {"from": user})
    tx.wait(1)
    assert beer.balanceOf(user) == 90
    assert coffee.balanceOf(user) == 10


def test_unbalanced_swap(beer, coffee, unbalanced_swap):
    user = accounts[1]
    tx = beer.getBeer({"from": unbalanced_swap.address})
    tx = beer.getBeer({"from": user})
    tx = coffee.getCoffee({"from": unbalanced_swap.address})
    tx.wait(1)
    tx = beer.approve(unbalanced_swap.address, 10, {"from": user})
    tx.wait(1)
    tx = unbalanced_swap.swapAforB(10, {"from": user})
    tx.wait(1)
    assert beer.balanceOf(user) == 90
    assert coffee.balanceOf(user) == 5


def test_decimal_swap(beer, coffee, decimal_swap):
    user = accounts[1]
    tx = beer.getBeer({"from": decimal_swap.address})
    tx = beer.getBeer({"from": user})
    tx = coffee.getCoffee({"from": decimal_swap.address})
    tx.wait(1)
    tx = beer.approve(decimal_swap.address, 10, {"from": user})
    tx.wait(1)
    tx = decimal_swap.swapAforB(10, {"from": user})
    tx.wait(1)
    assert beer.balanceOf(user) == 91
    assert coffee.balanceOf(user) == 6


def test_cannot_swap_without_allowance(beer, coffee, swap):
    user = accounts[1]
    tx = beer.getBeer({"from": swap.address})
    tx = beer.getBeer({"from": user})
    tx = coffee.getCoffee({"from": swap.address})
    tx.wait(1)
    tx = beer.approve(swap.address, 0, {"from": user})
    tx.wait(1)
    with brownie.reverts():
        tx = swap.swapAforB(10, {"from": user})
        tx.wait(1)

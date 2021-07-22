#!/usr/bin/python3

import pytest
from brownie_tokens import MintableForkToken
from brownie import Contract

USD_AMOUNT = 1000


@pytest.fixture(scope="session")
def dai():
    yield MintableForkToken('0x6B175474E89094C44Da98b954EedeAC495271d0F')


@pytest.fixture(scope="session")
def usdc():
    yield MintableForkToken('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')


@pytest.fixture(scope="session")
def usdt():
    yield MintableForkToken('0xdAC17F958D2ee523a2206206994597C13D831ec7')


@pytest.fixture(scope="session")
def _3Crv():
    yield Contract('0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490')


@pytest.fixture(scope="session")
def gauge():
    yield Contract('0xbFcF63294aD7105dEa65aA58F8AE5BE2D9d0952A')


@pytest.fixture(scope="session")
def margo(accounts):
    yield accounts[0]


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def zap(deposit_and_stake_zap, margo):
    return deposit_and_stake_zap.deploy({'from': margo})


@pytest.fixture(scope="module", autouse=True)
def mint(margo, dai, usdc, usdt):
    dai._mint_for_testing(margo.address, USD_AMOUNT * 10 ** 18)
    usdc._mint_for_testing(margo.address, USD_AMOUNT * 10 ** 6)
    usdt._mint_for_testing(margo.address, USD_AMOUNT * 10 ** 6)


@pytest.fixture(scope="module", autouse=True)
def approvals(zap, margo, dai, usdc, usdt, gauge):
    dai.approve(zap.address, 2 ** 256 - 1, {'from': margo})
    usdc.approve(zap.address, 2 ** 256 - 1, {'from': margo})
    usdt.approve(zap.address, 2 ** 256 - 1, {'from': margo})
    gauge.set_approve_deposit(zap.address, True, {'from': margo})

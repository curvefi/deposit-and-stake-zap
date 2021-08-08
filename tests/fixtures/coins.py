import pytest
from brownie import Contract, ETH_ADDRESS, ZERO_ADDRESS
from brownie_tokens import MintableForkToken


WRAPPED_COIN_METHODS = {
    "ATokenMock": {"get_rate": "_get_rate", "mint": "mint"},
    "cERC20": {"get_rate": "exchangeRateStored", "mint": "mint"},
    "IdleToken": {"get_rate": "tokenPrice", "mint": "mintIdleToken"},
    "renERC20": {"get_rate": "exchangeRateCurrent"},
    "yERC20": {"get_rate": "getPricePerFullShare", "mint": "deposit"},
    "aETH": {"get_rate": "ratio"},
    "rETH": {"get_rate": "getExchangeRate"},
}


# public fixtures - these can be used when testing


@pytest.fixture(scope="module")
def wrapped_coins(pool_data, _underlying_coins):
    return _wrapped(pool_data, _underlying_coins)


@pytest.fixture(scope="module")
def underlying_coins(_underlying_coins, _base_coins):
    if _base_coins:
        return _underlying_coins[:1] + _base_coins
    else:
        return _underlying_coins


@pytest.fixture(scope="module")
def lp_token(pool_data):
    return Contract(pool_data['lp_token_address'])


# private API below


class _MintableTestToken(MintableForkToken):
    def __init__(self, address, pool_data=None):
        super().__init__(address)

        # standardize mint / rate methods
        if pool_data is not None and "wrapped_contract" in pool_data:
            fn_names = WRAPPED_COIN_METHODS[pool_data["wrapped_contract"]]
            for target, attr in fn_names.items():
                if hasattr(self, attr) and target != attr:
                    setattr(self, target, getattr(self, attr))


def _wrapped(pool_data, underlying_coins):
    coins = []

    if not pool_data.get("wrapped_contract"):
        return underlying_coins

    for i, coin_data in enumerate(pool_data["coins"]):
        if not coin_data.get("wrapped_decimals"):
            coins.append(underlying_coins[i])
        else:
            coins.append(_MintableTestToken(coin_data["wrapped_address"], pool_data))
    return coins


def _underlying(pool_data):
    coins = []

    for data in pool_data["coins"]:
        if data.get("underlying_address") == ETH_ADDRESS:
            coins.append(ETH_ADDRESS)
        else:
            coins.append(
                _MintableTestToken(
                    data.get("underlying_address", data.get("wrapped_address")), pool_data
                )
            )

    return coins


# private fixtures used for setup in other fixtures - do not use in tests!


@pytest.fixture(scope="module")
def _underlying_coins(pool_data):
    return _underlying(pool_data)


@pytest.fixture(scope="module")
def _base_coins(base_pool_data):
    if base_pool_data is None:
        return []
    return _underlying(base_pool_data)

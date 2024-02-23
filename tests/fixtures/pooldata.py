import pytest
import brownie
from brownie import Contract, ZERO_ADDRESS

# gusd
gusd_token_address = "0xD2967f45c4f384DEEa880F807Be904762a3DeA07"
gusd_gauge_addresses = "0xC5cfaDA84E902aD92DD40194f0883ad49639b023"

# susd
susd_token_address = '0xC25a3A3b969415c80451098fa907EC722572917F'
susd_gauge_address = '0xA90996896660DEcC6E997655E065b23788857849'


@pytest.fixture(scope="module")
def swap_address(pool_data):
    return pool_data['swap_address']


@pytest.fixture(scope="module")
def token_address(pool_data):
    return pool_data['lp_token_address']


@pytest.fixture(scope="module")
def gauge_address(pool_data):
    return pool_data['gauge_addresses'][0]


@pytest.fixture(scope="module")
def deposit_address(pool_data):
    return pool_data['zap_address'] if 'zap_address' in pool_data else pool_data['swap_address']


@pytest.fixture(scope="module")
def other_token_address(pool_data):
    return gusd_token_address if gusd_token_address != pool_data["lp_token_address"] else susd_token_address


@pytest.fixture(scope="module")
def other_gauge_address(pool_data):
    return gusd_gauge_addresses if gusd_gauge_addresses != pool_data["gauge_addresses"][0] else susd_gauge_address


@pytest.fixture(scope="module")
def gauge(gauge_address):
    return Contract(gauge_address)


@pytest.fixture(scope="module")
def underlying_decimals(pool_data, base_pool_data):
    # number of decimal places for each underlying coin in the active pool
    decimals = [i.get("decimals", i.get("wrapped_decimals")) for i in pool_data["coins"]]

    if base_pool_data is None:
        return decimals
    base_decimals = [i.get("decimals", i.get("wrapped_decimals")) for i in base_pool_data["coins"]]
    return decimals[:-1] + base_decimals


@pytest.fixture(scope="module")
def wrapped_decimals(pool_data):
    # number of decimal places for each wrapped coin in the active pool
    yield [i.get("wrapped_decimals", i.get("decimals")) for i in pool_data["coins"]]


@pytest.fixture(scope="module")
def wrapped_amounts_to_mint(wrapped_decimals):
    return [100 * 10 ** i for i in wrapped_decimals]


@pytest.fixture(scope="module")
def underlying_amounts_to_mint(underlying_decimals):
    return [100 * 10 ** i for i in underlying_decimals]


@pytest.fixture(scope="module")
def wrong_amounts_to_mint():
    return [100 * 10 ** 18] * 5


# Different amounts are needed to always pass test_wrong_order_of_coins
@pytest.fixture(scope="module")
def wrapped_amounts(wrapped_decimals, n_coins_wrapped):
    return [(10 + i) * 10 ** wrapped_decimals[i] for i in range(n_coins_wrapped)]


# Different amounts are needed to always pass test_wrong_order_of_coins
@pytest.fixture(scope="module")
def underlying_amounts(underlying_decimals, n_coins_underlying):
    return [(10 + i) * 10 ** underlying_decimals[i] for i in range(n_coins_underlying)]


@pytest.fixture(scope="module")
def n_coins_wrapped(wrapped_decimals):
    return len(wrapped_decimals)


@pytest.fixture(scope="module")
def n_coins_underlying(underlying_decimals):
    yield len(underlying_decimals)


@pytest.fixture(scope="module")
def value_wrapped(wrapped_amounts, wrapped_coins):
    return wrapped_amounts[wrapped_coins.index(brownie.ETH_ADDRESS)] if brownie.ETH_ADDRESS in wrapped_coins else 0


@pytest.fixture(scope="module")
def value_underlying(underlying_amounts, underlying_coins):
    return underlying_amounts[underlying_coins.index(brownie.ETH_ADDRESS)] if brownie.ETH_ADDRESS in underlying_coins else 0


@pytest.fixture(scope="module")
def use_underlying(pool_data):
    if pool_data['swap_address'] in [
        "0xDeBF20617708857ebe4F679508E7b7863a8A8EeE",  # aave
        "0xeb16ae0052ed37f479f7fe63849198df1765a733",  # saave
        "0x2dded6Da1BF5DBdF597C45fcFaa3194e53EcfeAF",  # ib
        "0x8301AE4fc9c624d1D396cbDAa1ed877821D7C511",  # crveth (use_eth)
        "0xB576491F1E6e5E62f1d8F26062Ee822B40B0E0d4",  # cvxeth (use_eth)
    ]:
        return True

    return False


@pytest.fixture(scope="module")
def is_meta(pool_data):
    return "meta" in pool_data.get("pool_types", [])


@pytest.fixture(scope="module")
def factory_pool_address(pool_data):
    return pool_data["swap_address"] if "factory" in pool_data.get("pool_types", []) else ZERO_ADDRESS


@pytest.fixture(scope="module")
def use_dynarray(pool_data):
    ng_pools = [
        "0x6685fcfce05e7502bf9f0aa03b36025b09374726",  # vETH/ETH
        "0x383e6b4437b59fff47b619cba855ca29342a8559",  # PayPool
        "0x9e10f9fb6f0d32b350cee2618662243d4f24c64a",  # mkUSD
    ]
    if pool_data['swap_address'] in ng_pools:
        return True

    return False

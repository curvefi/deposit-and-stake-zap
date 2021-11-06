import pytest
import brownie
from brownie import Contract

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
def deposit_address(pool_data, has_zap):
    return pool_data['zap_address'] if has_zap else pool_data['swap_address']


@pytest.fixture(scope="module")
def other_token_address(pool_data):
    return gusd_token_address if gusd_token_address != pool_data["lp_token_address"] else susd_token_address


@pytest.fixture(scope="module")
def other_gauge_address(pool_data):
    return gusd_gauge_addresses if gusd_gauge_addresses != pool_data["gauge_addresses"][0] else gusd_token_address


@pytest.fixture(scope="module")
def gauge(gauge_address):
    return Contract(gauge_address)


@pytest.fixture(scope="module")
def has_zap(pool_data):
    return 'zap_address' in pool_data


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
def wrapped_amounts(wrapped_decimals, n_coins_wrapped):
    return [10 * 10 ** i for i in wrapped_decimals] + [0] * (5 - n_coins_wrapped)


@pytest.fixture(scope="module")
def underlying_amounts(underlying_decimals, n_coins_underlying):
    return [10 * 10 ** i for i in underlying_decimals] + [0] * (5 - n_coins_underlying)


@pytest.fixture(scope="module")
def n_coins_wrapped(wrapped_decimals):
    return len(wrapped_decimals)


@pytest.fixture(scope="module")
def n_coins_underlying(underlying_decimals):
    yield len(underlying_decimals)


@pytest.fixture(scope="module")
def value_wrapped(wrapped_amounts, wrapped_coins):
    return wrapped_amounts[0] if brownie.ETH_ADDRESS in wrapped_coins else 0


@pytest.fixture(scope="module")
def value_underlying(underlying_amounts, underlying_coins):
    return underlying_amounts[0] if brownie.ETH_ADDRESS in underlying_coins else 0


@pytest.fixture(scope="module")
def is_meta(pool_data):
    return "meta" in pool_data.get("pool_types", [])


@pytest.fixture(scope="module")
def is_v1(pool_data):
    return pool_data['lp_contract'] == 'CurveTokenV1'

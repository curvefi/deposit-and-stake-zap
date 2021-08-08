import pytest


@pytest.fixture(scope="module")
def zap(deposit_and_stake_zap, alice):
    return deposit_and_stake_zap.deploy({'from': alice})

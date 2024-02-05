import pytest


@pytest.fixture(scope="module")
def zap(DepositAndStakeZap, alice):
    return DepositAndStakeZap.deploy({'from': alice})

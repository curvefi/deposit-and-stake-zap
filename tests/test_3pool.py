import brownie

# 3pool
swap_address = '0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7'
token_address = '0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490'
gauge_address = '0xbFcF63294aD7105dEa65aA58F8AE5BE2D9d0952A'

# susd
other_swap_address = '0xA5407eAE9Ba41422680e2e00537571bcC53efBfD'
other_token_address = '0xC25a3A3b969415c80451098fa907EC722572917F'
other_gauge_address = '0xA90996896660DEcC6E997655E065b23788857849'

MAX_UINT256 = 2 ** 256 - 1
AMOUNTS = [100 * 10 ** 18, 100 * 10 ** 6, 100 * 10 ** 6, 0, 0, 0, 0, 0, 0, 0]

def test_balance(zap, margo, gauge):
    zap.deposit_and_stake(swap_address, token_address, gauge_address, 3, AMOUNTS, 0, True, {'from': margo})

    assert gauge.balanceOf(margo.address) > 0


def test_approve(zap, margo, dai, usdc, usdt, _3Crv):
    zap.deposit_and_stake(swap_address, token_address, gauge_address, 3, AMOUNTS, 0, True, {'from': margo})

    assert dai.allowance(zap.address, swap_address) == MAX_UINT256
    assert usdc.allowance(zap.address, swap_address) == MAX_UINT256 - (100 * 10 ** 6)
    assert usdt.allowance(zap.address, swap_address) == MAX_UINT256
    assert _3Crv.allowance(zap.address, gauge_address) > MAX_UINT256 / 2


def test_token_mismatch(zap, margo):
    with brownie.reverts("dev: swap-token mismatch"):
        zap.deposit_and_stake(swap_address, other_token_address, gauge_address, 3, AMOUNTS, 0, True, {'from': margo})


def test_gauge_mismatch(zap, margo):
    with brownie.reverts():
        zap.deposit_and_stake(swap_address, token_address, other_gauge_address, 3, AMOUNTS, 0, True, {'from': margo})


def test_token_and_gauge_mismatch(zap, margo):
    with brownie.reverts("dev: swap-token mismatch"):
        zap.deposit_and_stake(swap_address, other_token_address, other_gauge_address, 3, AMOUNTS, 0, True, {'from': margo})


def test_n_coins_too_high(zap, margo):
    with brownie.reverts():
        zap.deposit_and_stake(swap_address, other_token_address, gauge_address, 4, AMOUNTS, 0, True, {'from': margo})


def test_n_coins_too_low(zap, margo):
    with brownie.reverts():
        zap.deposit_and_stake(swap_address, other_token_address, gauge_address, 2, AMOUNTS, 0, True, {'from': margo})


def test_min_amount_too_high(zap, margo):
    with brownie.reverts():
        zap.deposit_and_stake(swap_address, token_address, gauge_address, 3, AMOUNTS, MAX_UINT256, True, {'from': margo})

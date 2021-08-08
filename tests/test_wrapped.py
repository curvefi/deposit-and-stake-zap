import pytest
import brownie

pytestmark = pytest.mark.usefixtures("mint_margo", "approve_margo")


def test_balance(
        zap, margo, swap_address, token_address, gauge_address,
        n_coins_wrapped, wrapped_amounts, is_v1, value_wrapped, gauge
):
    zap.deposit_and_stake(
        swap_address, token_address, gauge_address, n_coins_wrapped, wrapped_amounts, 0, is_v1,
        {'from': margo, 'value': value_wrapped}
    )

    assert gauge.balanceOf(margo.address) > 0


def test_approve(
        zap, margo, swap_address, token_address, gauge_address, n_coins_wrapped,
        wrapped_amounts, is_v1, value_wrapped, wrapped_coins, lp_token
):
    zap.deposit_and_stake(
        swap_address, token_address, gauge_address, n_coins_wrapped, wrapped_amounts, 0, is_v1,
        {'from': margo, 'value': value_wrapped}
    )

    for coin in wrapped_coins:
        if coin == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
            continue
        assert coin.allowance(zap.address, swap_address) > 2 ** 255

    assert lp_token.allowance(zap.address, gauge_address) > 2 ** 255


def test_token_mismatch(
        zap, margo, swap_address, other_token_address, gauge_address,
        n_coins_wrapped, wrapped_amounts, is_v1, value_wrapped
):
    with brownie.reverts("dev: swap-token mismatch"):
        zap.deposit_and_stake(
            swap_address, other_token_address, gauge_address, n_coins_wrapped, wrapped_amounts, 0, is_v1,
            {'from': margo, 'value': value_wrapped}
        )


def test_gauge_mismatch(
        zap, margo, swap_address, token_address, other_gauge_address,
        n_coins_wrapped, wrapped_amounts, is_v1, value_wrapped
):
    with brownie.reverts():
        zap.deposit_and_stake(
            swap_address, token_address, other_gauge_address, n_coins_wrapped, wrapped_amounts, 0, is_v1,
            {'from': margo, 'value': value_wrapped}
        )


def test_n_coins_too_high(
        zap, margo, swap_address, token_address, gauge_address,
        n_coins_wrapped, wrapped_amounts, is_v1, value_wrapped
):
    with brownie.reverts():
        zap.deposit_and_stake(
            swap_address, token_address, gauge_address, n_coins_wrapped + 1, wrapped_amounts, 0, is_v1,
            {'from': margo, 'value': value_wrapped}
        )


def test_n_coins_too_low(
        zap, margo, swap_address, token_address, gauge_address,
        n_coins_wrapped, wrapped_amounts, is_v1, value_wrapped
):
    with brownie.reverts():
        zap.deposit_and_stake(
            swap_address, token_address, gauge_address, n_coins_wrapped - 1, wrapped_amounts, 0, is_v1,
            {'from': margo, 'value': value_wrapped}
        )

import pytest
import brownie

pytestmark = pytest.mark.usefixtures("mint_margo", "approve_margo")


def test_balance(
        zap, margo, deposit_address, token_address, gauge_address, n_coins_underlying,
        underlying_amounts, is_v1, value_underlying, is_meta, has_zap, gauge
):
    if is_meta:
        zap.deposit_and_stake_underlying_meta(
            deposit_address, token_address, gauge_address, n_coins_underlying, underlying_amounts, 0, is_v1,
            {'from': margo, 'value': value_underlying}
        )
    elif has_zap:
        zap.deposit_and_stake_underlying_zap(
            deposit_address, token_address, gauge_address, n_coins_underlying, underlying_amounts, 0, is_v1,
            {'from': margo, 'value': value_underlying}
        )
    else:
        # aave, saave, ib
        zap.deposit_and_stake_underlying(
            deposit_address, token_address, gauge_address, n_coins_underlying, underlying_amounts, 0, is_v1,
            {'from': margo, 'value': value_underlying}
        )

    assert gauge.balanceOf(margo.address) > 0


def test_approve(
        zap, margo, deposit_address, token_address, gauge_address, n_coins_underlying,
        underlying_amounts, is_v1, value_underlying, is_meta, has_zap, underlying_coins, lp_token
):
    if is_meta:
        zap.deposit_and_stake_underlying_meta(
            deposit_address, token_address, gauge_address, n_coins_underlying, underlying_amounts, 0, is_v1,
            {'from': margo, 'value': value_underlying}
        )
    elif has_zap:
        zap.deposit_and_stake_underlying_zap(
            deposit_address, token_address, gauge_address, n_coins_underlying, underlying_amounts, 0, is_v1,
            {'from': margo, 'value': value_underlying}
        )
    else:
        # aave, saave, ib
        zap.deposit_and_stake_underlying(
            deposit_address, token_address, gauge_address, n_coins_underlying, underlying_amounts, 0, is_v1,
            {'from': margo, 'value': value_underlying}
        )

    for coin in underlying_coins:
        if coin == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
            continue
        assert coin.allowance(zap.address, deposit_address) > 2 ** 255

    assert lp_token.allowance(zap.address, gauge_address) > 2 ** 255


def test_token_mismatch(
        zap, margo, deposit_address, other_token_address, gauge_address, n_coins_underlying,
        underlying_amounts, is_v1, value_underlying, is_meta, has_zap,
):
    with brownie.reverts("dev: swap-token mismatch"):
        if is_meta:
            zap.deposit_and_stake_underlying_meta(
                deposit_address, other_token_address, gauge_address, n_coins_underlying, underlying_amounts, 0, is_v1,
                {'from': margo, 'value': value_underlying}
            )
        elif has_zap:
            zap.deposit_and_stake_underlying_zap(
                deposit_address, other_token_address, gauge_address, n_coins_underlying, underlying_amounts, 0, is_v1,
                {'from': margo, 'value': value_underlying}
            )
        else:
            # aave, saave, ib
            zap.deposit_and_stake_underlying(
                deposit_address, other_token_address, gauge_address, n_coins_underlying, underlying_amounts, 0, is_v1,
                {'from': margo, 'value': value_underlying}
            )


def test_gauge_mismatch(
        zap, margo, deposit_address, token_address, other_gauge_address, n_coins_underlying,
        underlying_amounts, is_v1, value_underlying, is_meta, has_zap,
):
    with brownie.reverts():
        if is_meta:
            zap.deposit_and_stake_underlying_meta(
                deposit_address, token_address, other_gauge_address, n_coins_underlying, underlying_amounts, 0, is_v1,
                {'from': margo, 'value': value_underlying}
            )
        elif has_zap:
            zap.deposit_and_stake_underlying_zap(
                deposit_address, token_address, other_gauge_address, n_coins_underlying, underlying_amounts, 0, is_v1,
                {'from': margo, 'value': value_underlying}
            )
        else:
            # aave, saave, ib
            zap.deposit_and_stake_underlying(
                deposit_address, token_address, other_gauge_address, n_coins_underlying, underlying_amounts, 0, is_v1,
                {'from': margo, 'value': value_underlying}
            )


def test_n_coins_too_high(
        zap, margo, deposit_address, token_address, gauge_address, n_coins_underlying,
        underlying_amounts, is_v1, value_underlying, is_meta, has_zap,
):
    with brownie.reverts():
        if is_meta:
            zap.deposit_and_stake_underlying_meta(
                deposit_address, token_address, gauge_address, n_coins_underlying + 1, underlying_amounts, 0, is_v1,
                {'from': margo, 'value': value_underlying}
            )
        elif has_zap:
            zap.deposit_and_stake_underlying_zap(
                deposit_address, token_address, gauge_address, n_coins_underlying + 1, underlying_amounts, 0, is_v1,
                {'from': margo, 'value': value_underlying}
            )
        else:
            # aave, saave, ib
            zap.deposit_and_stake_underlying(
                deposit_address, token_address, gauge_address, n_coins_underlying + 1, underlying_amounts, 0, is_v1,
                {'from': margo, 'value': value_underlying}
            )


def test_n_coins_too_low(
        zap, margo, deposit_address, token_address, gauge_address, n_coins_underlying,
        underlying_amounts, is_v1, value_underlying, is_meta, has_zap,
):
    with brownie.reverts():
        if is_meta:
            zap.deposit_and_stake_underlying_meta(
                deposit_address, token_address, gauge_address, n_coins_underlying - 1, underlying_amounts, 0, is_v1,
                {'from': margo, 'value': value_underlying}
            )
        elif has_zap:
            zap.deposit_and_stake_underlying_zap(
                deposit_address, token_address, gauge_address, n_coins_underlying - 1, underlying_amounts, 0, is_v1,
                {'from': margo, 'value': value_underlying}
            )
        else:
            # aave, saave, ib
            zap.deposit_and_stake_underlying(
                deposit_address, token_address, gauge_address, n_coins_underlying - 1, underlying_amounts, 0, is_v1,
                {'from': margo, 'value': value_underlying}
            )

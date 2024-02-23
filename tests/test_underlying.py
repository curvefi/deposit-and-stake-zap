import pytest
import brownie

pytestmark = pytest.mark.usefixtures("mint_margo", "approve_margo")


def test_balance(
        zap, margo, deposit_address, token_address, gauge_address, n_coins_underlying,
        underlying_coin_addresses, underlying_amounts, value_underlying, gauge, use_underlying,
        use_dynarray, factory_pool_address
):
    assert gauge.balanceOf(margo.address) == 0

    zap.deposit_and_stake(
        deposit_address,
        token_address,
        gauge_address,
        n_coins_underlying,
        underlying_coin_addresses,
        underlying_amounts,
        0,
        use_underlying,
        use_dynarray,
        factory_pool_address,
        {'from': margo, 'value': value_underlying}
    )

    assert gauge.balanceOf(margo.address) > 0
    assert gauge.balanceOf(deposit_address) == 0


def test_approve(
        zap, margo, deposit_address, token_address, gauge_address, n_coins_underlying, underlying_coin_addresses,
        underlying_amounts, value_underlying, underlying_coins, lp_token, use_underlying, use_dynarray,
        factory_pool_address
):
    for coin in underlying_coins:
        if coin == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
            continue
        assert coin.allowance(zap.address, deposit_address) == 0

    assert lp_token.allowance(zap.address, gauge_address) == 0

    zap.deposit_and_stake(
        deposit_address,
        token_address,
        gauge_address,
        n_coins_underlying,
        underlying_coin_addresses,
        underlying_amounts,
        0,
        use_underlying,
        use_dynarray,
        factory_pool_address,
        {'from': margo, 'value': value_underlying}
    )

    for coin in underlying_coins:
        if coin == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
            continue
        assert coin.allowance(zap.address, deposit_address) > 2 ** 255

    assert lp_token.allowance(zap.address, gauge_address) > 2 ** 255


def test_token_mismatch(
        zap, margo, deposit_address, other_token_address, gauge_address, n_coins_underlying,
        underlying_coin_addresses, underlying_amounts, value_underlying, use_underlying,
        use_dynarray, factory_pool_address
):
    with brownie.reverts():
        zap.deposit_and_stake(
            deposit_address,
            other_token_address,
            gauge_address,
            n_coins_underlying,
            underlying_coin_addresses,
            underlying_amounts,
            0,
            use_underlying,
            use_dynarray,
            factory_pool_address,
            {'from': margo, 'value': value_underlying}
        )


def test_gauge_mismatch(
        zap, margo, deposit_address, token_address, other_gauge_address, n_coins_underlying,
        underlying_coin_addresses, underlying_amounts, value_underlying, use_underlying,
        use_dynarray, factory_pool_address
):
    with brownie.reverts():
        zap.deposit_and_stake(
            deposit_address,
            token_address,
            other_gauge_address,
            n_coins_underlying,
            underlying_coin_addresses,
            underlying_amounts,
            0,
            use_underlying,
            use_dynarray,
            factory_pool_address,
            {'from': margo, 'value': value_underlying}
        )


def test_n_coins_too_high(
        zap, margo, deposit_address, token_address, gauge_address, n_coins_underlying,
        underlying_coin_addresses, underlying_amounts, value_underlying, use_underlying,
        use_dynarray, factory_pool_address
):
    with brownie.reverts():
        zap.deposit_and_stake(
            deposit_address,
            token_address,
            gauge_address,
            n_coins_underlying + 1,
            underlying_coin_addresses,
            underlying_amounts,
            0,
            use_underlying,
            use_dynarray,
            factory_pool_address,
            {'from': margo, 'value': value_underlying}
        )


def test_n_coins_too_low(
        zap, margo, deposit_address, token_address, gauge_address, n_coins_underlying,
        underlying_coin_addresses, underlying_amounts, value_underlying, use_underlying,
        use_dynarray, factory_pool_address
):
    with brownie.reverts():
        zap.deposit_and_stake(
            deposit_address,
            token_address,
            gauge_address,
            n_coins_underlying - 1,
            underlying_coin_addresses,
            underlying_amounts,
            0,
            use_underlying,
            use_dynarray,
            factory_pool_address,
            {'from': margo, 'value': value_underlying}
        )


def test_wrong_coins(
        zap, margo, deposit_address, token_address, gauge_address, n_coins_underlying,
        wrong_coin_addresses, underlying_amounts, value_underlying, use_underlying,
        use_dynarray, factory_pool_address
):
    with brownie.reverts():
        zap.deposit_and_stake(
            deposit_address,
            token_address,
            gauge_address,
            n_coins_underlying,
            wrong_coin_addresses,
            underlying_amounts,
            0,
            use_underlying,
            use_dynarray,
            factory_pool_address,
            {'from': margo, 'value': value_underlying}
        )


def test_wrong_order_of_coins(
        zap, margo, deposit_address, token_address, gauge_address, n_coins_underlying,
        underlying_coin_addresses_wrong_order, underlying_amounts, value_underlying,
        use_underlying, use_dynarray, factory_pool_address
):
    with brownie.reverts():
        zap.deposit_and_stake(
            deposit_address,
            token_address,
            gauge_address,
            n_coins_underlying,
            underlying_coin_addresses_wrong_order,
            underlying_amounts,
            0,
            use_underlying,
            use_dynarray,
            factory_pool_address,
            {'from': margo, 'value': value_underlying}
        )


def test_wrong_value(
        zap, margo, deposit_address, token_address, gauge_address, n_coins_underlying,
        underlying_coin_addresses, underlying_amounts, value_underlying, use_underlying,
        use_dynarray, factory_pool_address
):
    with brownie.reverts():
        zap.deposit_and_stake(
            deposit_address,
            token_address,
            gauge_address,
            n_coins_underlying,
            underlying_coin_addresses,
            underlying_amounts,
            0,
            use_underlying,
            use_dynarray,
            factory_pool_address,
            {'from': margo, 'value': 0 if value_underlying > 0 else 10**18}
        )


def test_wrong_use_underlying(
        zap, margo, deposit_address, token_address, gauge_address, n_coins_underlying,
        underlying_coin_addresses, underlying_amounts, value_underlying, use_underlying,
        use_dynarray, factory_pool_address
):
    if factory_pool_address == brownie.ZERO_ADDRESS:
        with brownie.reverts():
            zap.deposit_and_stake(
                deposit_address,
                token_address,
                gauge_address,
                n_coins_underlying,
                underlying_coin_addresses,
                underlying_amounts,
                0,
                not use_underlying,
                use_dynarray,
                factory_pool_address,
                {'from': margo, 'value': value_underlying}
            )

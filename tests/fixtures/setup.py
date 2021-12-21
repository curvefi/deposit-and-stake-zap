import pytest
from brownie import ETH_ADDRESS, accounts


def _mint(
        acct,
        wrapped_coins,
        wrapped_amounts_to_mint,
        underlying_coins,
        underlying_amounts_to_mint,
        wrong_coins,
        wrong_amounts_to_mint,
):
    for coin, amount in zip(wrapped_coins, wrapped_amounts_to_mint):
        if coin == ETH_ADDRESS:
            # in fork mode, we steal ETH from the wETH contract
            weth = accounts.at("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", True)
            weth.transfer(acct, amount)
            continue
        coin._mint_for_testing(acct, amount, {"from": acct})

    for coin, amount in zip(underlying_coins, underlying_amounts_to_mint):
        if coin in wrapped_coins:
            continue
        if coin == ETH_ADDRESS:
            weth = accounts.at("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", True)
            weth.transfer(acct, amount)
            continue
        coin._mint_for_testing(acct, amount, {"from": acct})

    for coin, amount in zip(wrong_coins, wrong_amounts_to_mint):
        if coin in wrapped_coins or coin in underlying_coins:
            continue
        coin._mint_for_testing(acct, amount, {"from": acct})


def _approve(owner, spender, *coins):
    for coin in set(x for i in coins for x in i):
        if coin == ETH_ADDRESS or coin.allowance(owner, spender) > 2 ** 255:
            continue
        coin.approve(spender, 2 ** 256 - 1, {"from": owner})


# pool setup fixtures

@pytest.fixture(scope="module")
def mint_margo(
        margo,
        underlying_coins,
        wrapped_coins,
        wrapped_amounts_to_mint,
        underlying_amounts_to_mint,
        wrong_coins,
        wrong_amounts_to_mint,
):
    _mint(
        margo,
        wrapped_coins,
        wrapped_amounts_to_mint,
        underlying_coins,
        underlying_amounts_to_mint,
        wrong_coins,
        wrong_amounts_to_mint,
    )


@pytest.fixture(scope="module")
def approve_margo(margo, zap, gauge, underlying_coins, wrapped_coins, wrong_coins):
    _approve(margo, zap.address, underlying_coins, wrapped_coins, wrong_coins)
    if hasattr(gauge, 'set_approve_deposit'):
        gauge.set_approve_deposit(zap.address, True, {'from': margo})

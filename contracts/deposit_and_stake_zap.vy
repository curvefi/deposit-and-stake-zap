# @version ^0.2.12
# A "zap" to deposit and stake Curve contract with one transaction
# (c) Curve.Fi, 2021

MAX_COINS: constant(int128) = 10

# External Contracts
interface ERC20:
    def transfer(_receiver: address, _amount: uint256): nonpayable
    def transferFrom(_sender: address, _receiver: address, _amount: uint256): nonpayable
    def approve(_spender: address, _amount: uint256): nonpayable
    def decimals() -> uint256: view
    def balanceOf(_owner: address) -> uint256: view

interface Pool:
    def coins(i: int128) -> address: view

interface PoolV1:
    def coins(i: uint256) -> address: view

interface Pool2:
    def add_liquidity(amounts: uint256[2], min_mint_amount: uint256): nonpayable

interface Pool3:
    def add_liquidity(amounts: uint256[3], min_mint_amount: uint256): nonpayable

interface Pool4:
    def add_liquidity(amounts: uint256[4], min_mint_amount: uint256): nonpayable

interface Pool5:
    def add_liquidity(amounts: uint256[5], min_mint_amount: uint256): nonpayable

interface Pool6:
    def add_liquidity(amounts: uint256[6], min_mint_amount: uint256): nonpayable

interface Pool7:
    def add_liquidity(amounts: uint256[7], min_mint_amount: uint256): nonpayable

interface Pool8:
    def add_liquidity(amounts: uint256[8], min_mint_amount: uint256): nonpayable

interface Pool9:
    def add_liquidity(amounts: uint256[9], min_mint_amount: uint256): nonpayable

interface Pool10:
    def add_liquidity(amounts: uint256[10], min_mint_amount: uint256): nonpayable

interface Gauge:
    def deposit(lp_token_amount: uint256, addr: address): nonpayable


allowance: HashMap[address, bool]


@external
@nonreentrant('lock')
def deposit_and_stake(pool: address, lp_token: address, gauge: address, n_coins: int128, amounts: uint256[10], min_mint_amount: uint256, is_v1: bool):
    assert n_coins >= 2, 'n_coins must be >=2'
    assert n_coins <= 10, 'n_coins must be <=10'

    # Первый заплатит за всех :)
    # Тут куча моментов, где этот первый (да и последующие) может обмануть. Перечислил ниже и расставил по коду метки,
    # где должен произойти revert предположительно. (Это же значит, что вообще всё везде откатится и в хэшмапе останется False?).
    # 1. pool не соответствует gauge.
    # 2. lp_token не соответствует gauge.
    # 3. n_coins > монет в пуле.
    # 4. n_coins < монет в пуле.
    # (см. REVERT №1,2,3,4)
    if not self.allowance[gauge]:
        self.allowance[gauge] = True

        # Ещё проблема. Если вдруг gauge поменяется, то повторный аппрув на монетки сломается?
        for i in range(MAX_COINS):
            if i >= n_coins:
                break

            in_coin: address = ZERO_ADDRESS
            if is_v1:
                in_coin = PoolV1(pool).coins(convert(i, uint256))  # <-- Читаю 2 раза REVERT №3
            else:
                in_coin = Pool(pool).coins(i)  # <-- Читаю 2 раза REVERT №3
            ERC20(in_coin).approve(pool, MAX_UINT256)

        ERC20(lp_token).approve(gauge, MAX_UINT256)


    # Transfer coins from owner
    for i in range(MAX_COINS):
        if i >= n_coins:
            break

        in_amount: uint256 = amounts[i]
        in_coin: address = ZERO_ADDRESS
        if is_v1:
            in_coin = PoolV1(pool).coins(convert(i, uint256))  # <-- Читаю 2 раза REVERT №3
        else:
            in_coin = Pool(pool).coins(i)  # <-- Читаю 2 раза REVERT №3

        if in_amount > 0:
            # "safeTransferFrom" which works for ERC20s which return bool or not
            _response: Bytes[32] = raw_call(
                in_coin,
                concat(
                    method_id("transferFrom(address,address,uint256)"),
                    convert(msg.sender, bytes32),
                    convert(self, bytes32),
                    convert(in_amount, bytes32),
                ),
                max_outsize=32,
            )  # dev: failed transfer
            if len(_response) > 0:
                assert convert(_response, bool)  # dev: failed transfer

    # Revert №4
    if n_coins == 2:
        Pool2(pool).add_liquidity([amounts[0], amounts[1]], min_mint_amount)
    elif n_coins == 3:
        Pool3(pool).add_liquidity([amounts[0], amounts[1], amounts[2]], min_mint_amount)
    elif n_coins == 4:
        Pool4(pool).add_liquidity([amounts[0], amounts[1], amounts[2], amounts[3]], min_mint_amount)
    elif n_coins == 5:
        Pool5(pool).add_liquidity([amounts[0], amounts[1], amounts[2], amounts[3], amounts[4]], min_mint_amount)
    elif n_coins == 6:
        Pool6(pool).add_liquidity([amounts[0], amounts[1], amounts[2], amounts[3], amounts[4], amounts[5]], min_mint_amount)
    elif n_coins == 7:
        Pool7(pool).add_liquidity([amounts[0], amounts[1], amounts[2], amounts[3], amounts[4], amounts[5], amounts[6]], min_mint_amount)
    elif n_coins == 8:
        Pool8(pool).add_liquidity([amounts[0], amounts[1], amounts[2], amounts[3], amounts[4], amounts[5], amounts[6], amounts[7]], min_mint_amount)
    elif n_coins == 9:
        Pool9(pool).add_liquidity([amounts[0], amounts[1], amounts[2], amounts[3], amounts[4], amounts[5], amounts[6], amounts[7], amounts[8]], min_mint_amount)
    elif n_coins == 10:
        Pool10(pool).add_liquidity([amounts[0], amounts[1], amounts[2], amounts[3], amounts[4], amounts[5], amounts[6], amounts[7], amounts[8], amounts[9]], min_mint_amount)

    lp_token_amount: uint256 = ERC20(lp_token).balanceOf(self)
    assert lp_token_amount > 0 # dev: swap-token mismatch

    Gauge(gauge).deposit(lp_token_amount, msg.sender) # REVERT №1 и №2

#!/usr/bin/python3

from brownie import deposit_and_stake_zap, accounts


def main():
    print(type(deposit_and_stake_zap))
    return deposit_and_stake_zap.deploy({'from': accounts[0]})

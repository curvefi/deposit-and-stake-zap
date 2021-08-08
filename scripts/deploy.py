#!/usr/bin/python3

from brownie import deposit_and_stake_zap, accounts


def main():
    return deposit_and_stake_zap.deploy({'from': accounts[0]})

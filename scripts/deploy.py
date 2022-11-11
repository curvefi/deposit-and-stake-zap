#!/usr/bin/python3

from brownie import network
from brownie import deposit_and_stake_zap, accounts


def main():
    txparams = {}
    if network.show_active() == 'mainnet':
        accounts.load('curve-tester')
        txparams.update({'priority_fee': '2 gwei'})
    else:
        accounts.load('curve-tester')
    txparams.update({'from': accounts[0]})
    return deposit_and_stake_zap.deploy(txparams)

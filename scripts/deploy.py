#!/usr/bin/python3

from brownie import network
from brownie import deposit_and_stake_zap, accounts


def main():
    txparams = {'from': accounts[0]}
    if network.show_active() == 'mainnet':
        accounts.load('babe')
        txparams.update({'from': accounts[0], 'priority_fee': '2 gwei'})
    return deposit_and_stake_zap.deploy(txparams)

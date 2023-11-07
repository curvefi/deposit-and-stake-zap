#!/usr/bin/python3

from brownie import network
from brownie import deposit_and_stake_zap, accounts


def main():
    txparams = {}
    if network.show_active() == 'mainnet':
        accounts.load('curve-deployer')
        txparams.update({'priority_fee': '2 gwei'})
    elif not network.show_active().endswith("-fork"):
        accounts.load('curve-deployer')
    txparams.update({'from': accounts[0]})
    return deposit_and_stake_zap.deploy(txparams)

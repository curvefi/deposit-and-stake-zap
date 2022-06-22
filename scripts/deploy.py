#!/usr/bin/python3

from brownie import network
from brownie import deposit_and_stake_zap, accounts


def main():
    txparams = {}
    if network.show_active() == 'mainnet':
        accounts.load('babe')
        txparams.update({'priority_fee': '2 gwei'})
    elif network.show_active() == 'polygon-main':
        accounts.load('babe')
    elif network.show_active() == 'avalanche':
        accounts.load('babe')
    txparams.update({'from': accounts[0]})
    return deposit_and_stake_zap.deploy(txparams)

# Deposit&Stake Zap

Smart contract which allows add liquidity and deposit into gauge in one transaction.

- Ethereum: [0xBFab8ebc836E1c4D81837798FC076D219C9a1855](https://etherscan.io/address/0xBFab8ebc836E1c4D81837798FC076D219C9a1855#code)
- Optimism: [0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD](https://optimistic.etherscan.io/address/0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD#code)
- Gnosis (xDai): [0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD](https://gnosisscan.io/address/0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD#code)
- Polygon: [0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD](https://polygonscan.com/address/0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD#code)
- Fantom: [0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD](https://ftmscan.com/address/0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD#code)
- Kava: [0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD](https://explorer.kava.io/address/0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD/contracts)
- Arbitrum: [0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD](https://arbiscan.io/address/0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD#code)
- Avalanche: [0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD](https://snowtrace.io/address/0x37c5ab57AF7100Bdc9B668d766e193CCbF6614FD#code)
- Base: [0x69522fb5337663d3B4dFB0030b881c1A750Adb4f](https://basescan.org/address/0x69522fb5337663d3B4dFB0030b881c1A750Adb4f#code)
- BSC: [0x4f37A9d177470499A2dD084621020b023fcffc1F](https://bscscan.com/address/0x4f37A9d177470499A2dD084621020b023fcffc1F#code)
- Fraxtal: [0x0fE38dCC905eC14F6099a83Ac5C93BF2601300CF](https://fraxscan.com/address/0x0fE38dCC905eC14F6099a83Ac5C93BF2601300CF#code)


## Testing and Development

### Dependencies

- [python3](https://www.python.org/downloads/release/python-368/) version 3.6 or greater, python3-dev
- [vyper](https://github.com/vyperlang/vyper) version [0.3.0](https://github.com/vyperlang/vyper/releases/tag/v0.3.0)
- [brownie](https://github.com/iamdefinitelyahuman/brownie) - tested with version [1.17.0](https://github.com/eth-brownie/brownie/releases/tag/v1.17.0)
- [brownie-token-tester](https://github.com/iamdefinitelyahuman/brownie-token-tester) - tested with version [0.3.2](https://github.com/iamdefinitelyahuman/brownie-token-tester/releases/tag/v0.3.2)
- [ganache-cli](https://github.com/trufflesuite/ganache-cli) - tested with version [6.12.2](https://github.com/trufflesuite/ganache-cli/releases/tag/v6.12.2)

### Setup

To get started, first create and initialize a Python [virtual environment](https://docs.python.org/3/library/venv.html). Next, clone the repo and install the developer dependencies:

```bash
git clone https://github.com/curvefi/deposit-and-stake-zap.git
cd deposit-and-stake-zap
pip install -r requirements.txt
```

### Running the Tests

To run the entire suite:

```bash
brownie test --network mainnet-fork
```

To run for particular pools:

```bash
brownie test --pools 3pool,compound,aave,musd,tusd,tricrypto2,cvxeth,veth,usdv,paypool,mkusd --network mainnet-hardhat-fork
```

To run only for underlying/wrapped coins:

```bash
brownie test --coins underlying --network mainnet-fork

or

brownie test --coins wrapped --network mainnet-fork
```

### Deploy
```bash
brownie run deploy --network <id>
```

## License

This project is licensed under the [MIT license](LICENSE).

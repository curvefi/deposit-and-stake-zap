# Deposit&Stake Zap

Smart contract which allows add liquidity and deposit into gauge in one transaction.

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
git clone https://github.com/Macket/deposit_and_stake_zap  <--- CHANGE
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
brownie test --pools 3pool,compound,aave,usdn,mim,tricrypto2,crveth --network mainnet-fork
```

To run only for underlying/wrapped coins:

```bash
brownie test --coins underlying --network mainnet-fork

or

brownie test --coins wrapped --network mainnet-fork
```


## License

This project is licensed under the [MIT license](LICENSE).

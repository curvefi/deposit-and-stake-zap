#!/usr/bin/python3
import json
import pytest
from pathlib import Path
from brownie.project.main import get_loaded_projects

POOLS = ['3pool', 'aave', 'aeth', 'bbtc', 'busd', 'compound', 'dusd', 'gusd', 'hbtc', 'husd', 'ib', 'link', 'musd', 'obtc',
         'pax', 'pbtc', 'ren', 'reth', 'rsv', 'saave', 'sbtc', 'seth', 'steth', 'susd', 'tbtc', 'usdk', 'usdn', 'usdp', 'usdt',
         'ust', 'y', 'tricrypto2', 'eurt', 'eurtusd', 'crveth', 'cvxeth', 'tusd']  # 'eurs'

LENDING_POOLS = ['compound', 'usdt', 'y', 'busd', 'pax', 'aave', 'saave', 'ib']
META_POOLS = ['gusd', 'husd', 'usdk', 'usdn', 'musd', 'rsv', 'tbtc', 'dusd', 'pbtc', 'bbtc', 'obtc', 'ust', 'usdp', 'eurtusd']
FACTORY_POOOLS = ['tusd']  # 'frax', 'lusd', 'busdv2', 'alusd', 'mim'
WETH_POOLS = ['tricrypto2', 'crveth', 'cvxeth']

pytest_plugins = [
    "fixtures.accounts",
    "fixtures.coins",
    "fixtures.deployments",
    "fixtures.pooldata",
    "fixtures.setup",
]

_pooldata = {}


def pytest_addoption(parser):
    parser.addoption("--coins", help="wrapped or underlying")
    parser.addoption("--pool", help="comma-separated list of pools to target")


def pytest_sessionstart():
    # load `pooldata.json` for each pool
    project = get_loaded_projects()[0]
    for path in [i for i in project._path.glob("contracts/pools/*") if i.is_dir()]:
        with path.joinpath("pooldata.json").open() as fp:
            _pooldata[path.name] = json.load(fp)
            _pooldata[path.name].update(name=path.name)

    for _, data in _pooldata.items():
        if "base_pool" in data:
            data["base_pool"] = _pooldata[data["base_pool"]]


def pytest_ignore_collect(path, config):
    project = get_loaded_projects()[0]
    path = Path(path).relative_to(project._path)
    test_file = path.parts[1]

    coins = config.getoption("coins") or 'all'

    if coins == 'wrapped' and test_file == 'test_underlying.py':
        return True

    if coins == 'underlying' and test_file == 'test_wrapped.py':
        return True

    if coins != 'wrapped' and coins != 'underlying' and coins != 'all':
        raise ValueError('Invalid --coins option. Must be wrapped or underlying')


def pytest_generate_tests(metafunc):
    project = get_loaded_projects()[0]
    path = Path(metafunc.definition.fspath).relative_to(project._path)
    test_file = path.parts[1]
    coins = metafunc.config.getoption("coins") or 'all'

    try:
        params = metafunc.config.getoption("pool").split(",")
    except Exception:
        params = POOLS if coins == 'wrapped' else LENDING_POOLS + META_POOLS + WETH_POOLS

    for pool in params:
        if pool not in POOLS:
            raise ValueError(f"Invalid pool name: {pool}")

    if test_file == 'test_underlying.py':
        params = list(filter(lambda pool: pool in LENDING_POOLS + META_POOLS + FACTORY_POOOLS + WETH_POOLS, params))

    metafunc.parametrize("pool_data", params, indirect=True, scope="session")


@pytest.fixture(autouse=True)
def isolation_setup(fn_isolation):
    pass


@pytest.fixture(scope="module")
def pool_data(request):
    return _pooldata[request.param]


@pytest.fixture(scope="module")
def base_pool_data(pool_data):
    return pool_data.get("base_pool", None)

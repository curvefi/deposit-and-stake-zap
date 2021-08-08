#!/usr/bin/python3
import json
import pytest
from pathlib import Path
from brownie.project.main import get_loaded_projects

POOLS = ['3pool', 'aave', 'aeth', 'bbtc', 'busd', 'compound', 'dusd', 'gusd', 'hbtc', 'husd', 'ib', 'link', 'musd', 'obtc',
         'pax', 'pbtc', 'ren', 'reth', 'rsv', 'saave', 'sbtc', 'seth', 'steth', 'susd', 'tbtc', 'usdk', 'usdn', 'usdp', 'usdt',
         'ust', 'y']  # 'eurs'

LENDING_POOLS = ['compound', 'usdt', 'y', 'busd', 'pax', 'aave', 'saave', 'ib']
META_POOLS = ['gusd', 'husd', 'usdk', 'usdn', 'musd', 'rsv', 'tbtc', 'dusd', 'pbtc', 'bbtc', 'obtc', 'ust', 'usdp']
#  'tusd', 'frax', 'lusd', 'busdv2', 'alusd', 'mim' ()

pytest_plugins = [
    "fixtures.accounts",
    "fixtures.coins",
    "fixtures.deployments",
    "fixtures.pooldata",
    "fixtures.setup",
]

_pooldata = {}


def pytest_addoption(parser):
    parser.addoption("--test_type", help="wrapped or underlying")
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

    test_type = config.getoption("test_type") or 'wrapped'

    if test_type == 'wrapped' and test_file == 'test_underlying.py':
        return True

    if test_type == 'underlying' and test_file == 'test_wrapped.py':
        return True

    if test_type != 'wrapped' and test_type != 'underlying':
        raise ValueError('Invalid --test_type option')


def pytest_generate_tests(metafunc):
    test_type = metafunc.config.getoption("test_type") or 'wrapped'

    try:
        params = metafunc.config.getoption("pool").split(",")
    except Exception:
        params = POOLS if test_type == 'wrapped' else LENDING_POOLS + META_POOLS

    if test_type == 'underlying':
        for pool in params:
            if pool not in LENDING_POOLS + META_POOLS:
                raise ValueError(f"Underlying test for {pool} pool is not available")

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

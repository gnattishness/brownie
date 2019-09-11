#!/usr/bin/python3

isolation_source = '''import pytest

@pytest.fixture(autouse=True)
def isolation({0}_isolation):
    pass

@pytest.fixture(scope="module", autouse=True)
def setup(accounts):
    accounts[0].transfer(accounts[1], "1 ether")

def test_isolation_first(accounts, web3):
    assert web3.eth.blockNumber == 1
    assert accounts[1].balance() == "101 ether"
    accounts[0].transfer(accounts[1], "1 ether")

def test_isolation_second(accounts, web3):
    assert web3.eth.blockNumber == {1}
    assert accounts[1].balance() == "10{1} ether"'''


def test_test_isolation(plugintester, web3):
    plugintester.makepyfile(isolation_source.format('fn', 1))
    result = plugintester.runpytest()
    result.assert_outcomes(passed=2)
    assert web3.eth.blockNumber == 0


def test_module_isolation(plugintester, web3):
    plugintester.makepyfile(isolation_source.format('module', 2))
    result = plugintester.runpytest()
    result.assert_outcomes(passed=2)
    assert web3.eth.blockNumber == 0
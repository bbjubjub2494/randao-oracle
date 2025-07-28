import pytest
from script.deploy import deploy
from contracts import RlpUtilsHarness

@pytest.fixture
def rlp_utils_harness_contract():
    return RlpUtilsHarness.deploy()

@pytest.fixture(scope="session")
def raffle_factory_contract():
    return deploy()

import pytest
from script.deploy import deploy
from contracts import RlpUtilsHarness

from moccasin.config import get_config

@pytest.fixture
def rlp_utils_harness_contract():
    return RlpUtilsHarness.deploy()

@pytest.fixture
def raffle_factory_contract():
    active_network = get_config().get_active_network()
    return active_network.manifest_named_contract('RaffleFactory')

import pytest
from script.deploy import deploy
from contracts import RlpUtilsHarness

@pytest.fixture
def rlp_utils_harness_contract():
    return RlpUtilsHarness.deploy()

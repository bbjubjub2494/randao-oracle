import time

import boa
import pytest
import rlp
import web3

from contracts import RaffleImplementation

from tests.util import get_block_header

@pytest.mark.staging
@pytest.mark.ignore_isolation
def test_live_lottery(raffle_factory_contract):
    w3 = web3.Web3(web3.HTTPProvider(boa.env._rpc._rpc_url))

    players = [boa.env.generate_address() for _ in range(100)]

    raffle_address = raffle_factory_contract.create(players, value=1)
    raffle_contract = RaffleImplementation.at(raffle_address)

    resolution_block = raffle_contract.resolution_block()
    while resolution_block >= w3.eth.block_number:
                   time.sleep(1)

    print(resolution_block)
    header = get_block_header(w3, resolution_block)
    raffle_contract.resolve(rlp.encode(header), players)

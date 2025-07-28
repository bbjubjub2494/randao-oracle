import boa
import pytest
import rlp
import hypothesis.strategies as st
from hypothesis import given, settings

from contracts import Raffle

@given(n_players=st.integers(min_value=1, max_value=100),
       blocks_to_mine=st.integers(min_value=0, max_value=8),
       mix_hash=st.binary(min_size=32, max_size=32))
def test_raffle(n_players, blocks_to_mine, mix_hash):
    mix_hash = bytes(32)  # FIXME force block headers to have the correct mixHash
    players = [boa.env.generate_address() for _ in range(n_players)]
    raffle_contract = Raffle.deploy(players, value=1)
    deploy_block_height = boa.env.evm.chain.get_block().header.block_number
    resolution_block_height = deploy_block_height + 5
    for _ in range(blocks_to_mine):
        block, _, _ = boa.env.evm.chain.build_block_with_transactions_and_withdrawals([])
        boa.env.evm.chain.import_block(block)
    boa.env.time_travel(blocks=blocks_to_mine)
    current_block_height = boa.env.evm.chain.get_block().header.block_number
    if current_block_height <= resolution_block_height:
        return
    boa.env.evm.patch.prev_hashes = reversed([boa.env.evm.chain.get_canonical_block_by_number(i).header.hash for i in range(current_block_height)])
    header = boa.env.evm.chain.get_canonical_block_by_number(resolution_block_height).header
    winner_index = int.from_bytes(mix_hash, 'big') % n_players
    winner = players[winner_index]
    assert boa.env.get_balance(winner) == 0
    raffle_contract.resolve(rlp.encode(header))
    assert boa.env.get_balance(winner) == 1

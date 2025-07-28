#pragma version ~=0.4.3

from contracts import RlpUtils
from contracts import IRaffle

from pcaversaccio.snekmate.src.snekmate.utils import block_hash as bh

implements: IRaffle

resolution_block: public(uint256)
players: public(DynArray[address,100])

@deploy
def __init__():
    # ensure the master copy is not used
    self.resolution_block = max_value(uint256)

@external
@payable
def setup(players: DynArray[address,100]):
    assert self.resolution_block == 0, "Raffle already setup"
    self.players = players
    self.resolution_block = block.number + 5

@external
def resolve(block_header: Bytes[1000]):
    assert keccak256(block_header) == bh._block_hash(self.resolution_block), "Invalid block header"
    randao: Bytes[32] = RlpUtils.extract_prevrandao(block_header)
    winner_index: uint256 = convert(randao, uint256) % len(self.players)
    winner: address = self.players[winner_index]
    selfdestruct(winner)

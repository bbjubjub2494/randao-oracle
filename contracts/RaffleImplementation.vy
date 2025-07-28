# pragma version ~=0.4.3

from contracts import RlpUtils
from contracts import IRaffle

from pcaversaccio.snekmate.src.snekmate.utils import block_hash as bh

implements: IRaffle

resolution_block: public(uint256)
players_hash: bytes32


@deploy
def __init__():
    # ensure the master copy is not used
    self.resolution_block = max_value(uint256)


@external
@payable
def setup(players: DynArray[address, 100]):
    assert self.resolution_block == 0, "Raffle already setup"
    self.players_hash = keccak256(abi_encode(players))
    self.resolution_block = block.number + 5


@external
def resolve(block_header: Bytes[1000], players: DynArray[address, 100]):
    assert keccak256(block_header) == bh._block_hash(
        self.resolution_block
    ), "Invalid block header"
    assert (
        keccak256(abi_encode(players)) == self.players_hash
    ), "Invalid players"

    # reset to save gas on duplicate transactions
    # as a bonus, this refunds some gas
    self.players_hash = empty(bytes32)

    randao: bytes32 = RlpUtils.extract_prevrandao(block_header)
    seed: bytes32 = keccak256(abi_encode(self, randao))
    winner_index: uint256 = convert(seed, uint256) % len(players)
    winner: address = players[winner_index]

    # transfer the prize to the winner
    # keep this last since it stops execution, and might destroy the contract
    selfdestruct(winner)

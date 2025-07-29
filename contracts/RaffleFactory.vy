# pragma version ~=0.4.3
# SPDX-License-Identifier: AGPL-3.0-only

interface IRaffle:
    def setup(players: DynArray[address, 100]): payable
    def resolve(block_header: Bytes[1000], players: DynArray[address, 100]): nonpayable

RAFFLE_IMPLEMENTATION: public(immutable(address))


@deploy
def __init__(raffle_implementation: address):
    RAFFLE_IMPLEMENTATION = raffle_implementation


@external
@payable
def create(players: DynArray[address, 100]) -> IRaffle:
    assert msg.value > 0, "No prize to raffle"

    raffle: IRaffle = IRaffle(create_minimal_proxy_to(RAFFLE_IMPLEMENTATION))
    extcall raffle.setup(players, value=msg.value)
    return raffle

from contracts import Raffle
import boa

def test_raffle():
    players = [
        boa.env.generate_address(),
        boa.env.generate_address(),
    ]
    raffle_contract = Raffle.deploy(players, value=1)
    raffle_contract.resolve(b"") # FIXME

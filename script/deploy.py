from contracts import RaffleFactory, RaffleImplementation
from moccasin.boa_tools import VyperContract


def deploy() -> VyperContract:
    implementation: VyperContract = RaffleImplementation.deploy()
    factory: VyperContract = RaffleFactory.deploy(implementation.address)
    return factory


def moccasin_main() -> VyperContract:
    return deploy()

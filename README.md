# Trustless Randomness Oracle on Ethereum

Work in progress.

This library allows obtaining random numbers on Ethereum itself, without no additional trust assumptions.
It uses the RANDAO output from the Ethereum consensus layer.

## Protocol

The protocol happens in two steps:

1. **Setup Step**: The operator of the raffle deploys a contract that holds the prize money.
   The contract records the list of participants and the number of a future block whose RANDAO output will be used to determine the winner.

2. **Resolution Step**: After the future block has been proposed, anyone can call the contract to resolve the raffle.
   The contract will use the RANDAO output from the specified block to select a winner from the list of participants.
   Since the RANDAO output is accessible directly from the EVM (except for the block after) the block header must be provided as an argument to the contract call. The contract ensures the integrity of the block header by comparing its hash against the hash provided by [EIP-2935]. On Ethereum Mainnet, this leaves more than a day for the transaction to happen. (27 hours, 18 minutes, 12 seconds minutes to be precise)

## Usage

The factory is deployed using [Deterministic Deployment Proxy] on Ethereum Mainnet, Gnosis Chain, and their testnets, at the following address:

```
TBD
```

Just call the `create` method to deploy a new raffle contract. The factory will return the address.
call `resolution_block` on the rafle contract to get the block number that will be used to resolve the raffle.
Then, after the block has been proposed, call `resolve` to provide the block header to transfer the prize to the winner.

Note that you need to provide the list of participants in both transactions. Since storage is expensive, the contract only stores the hash of the list.
    
For L2s, there is currently no general solution to access the L1 block hash. You may want to look at [anyrand vrf] which is more suitable to L2s.

[EIP-2935]: https://eips.ethereum.org/EIPS/eip-2935
[Deterministic Deployment Proxy]: https://github.com/Arachnid/deterministic-deployment-proxy
[anyrand vrf]: https://anyrand.com/

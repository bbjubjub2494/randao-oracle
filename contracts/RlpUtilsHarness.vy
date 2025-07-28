# pragma version ~=0.4.3

from contracts import RlpUtils


@external
@pure
def expect_list(input: Bytes[1000], offset: uint256 = 0) -> (uint256, uint256):
    return RlpUtils.rlp_expect_list(slice(input, offset, len(input) - offset))


@external
@pure
def skip_string(input: Bytes[1000], offset: uint256 = 0) -> uint256:
    return RlpUtils.rlp_skip_string(slice(input, offset, len(input) - offset))


@external
@pure
def extract_prevrandao(header: Bytes[1000]) -> bytes32:
    return RlpUtils.extract_prevrandao(header)

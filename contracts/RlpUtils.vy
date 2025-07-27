@pure
def rlp_expect_list(input: Bytes[1000]) -> (uint256, uint256):
    """
    Check if the input is a valid RLP-encoded list.
    Returns the length of the list and the number of bytes consumed in the prefix.
    """
    prefix_byte: uint256 = convert(slice(input, 0, 1), uint256)
    if prefix_byte < 192:
        raise "expected a list"
    elif prefix_byte < 248:
        return prefix_byte - 192, 1
    else:
        return self.decode_int(slice(slice(input, 1, 8), 0, prefix_byte - 247)), prefix_byte - 247 + 1

@pure
def rlp_skip_string(input: Bytes[1000]) -> uint256:
    """
    Skip the RLP-encoded string and return the number of bytes consumed.
    """
    prefix_byte: uint256 = convert(slice(input, 0, 1), uint256)
    if prefix_byte < 128:
        return 1
    elif prefix_byte < 184:
        return prefix_byte - 128 + 1
    elif prefix_byte < 192:
        return self.decode_int(slice(slice(input, 1, 8), 0, prefix_byte - 183)) + prefix_byte - 183 + 1
    else:
        raise "expected a string"

@pure
def decode_int(input: Bytes[8]) -> uint256:
    result: uint256 = 0
    for i: uint256 in range(len(input), bound=8):
        byte: uint256 = convert(slice(input, i, 1), uint256)
        result = (result << 8) | byte
    return result


MIXHASH_INDEX: constant(uint256) = 13 # index of mixHash in the block header

@pure
def extract_prevrandao(header: Bytes[1000]) -> Bytes[32]:
    """
    Extract the prevRandao value from the block header.
    """
    length: uint256 = 0
    offset: uint256 = 0
    length, offset = self.rlp_expect_list(header)
    header = slice(header, offset, len(header) - offset)
    assert length > MIXHASH_INDEX, "Header does not contain enough elements"
    for i: uint256 in range(MIXHASH_INDEX):
        offset = self.rlp_skip_string(header)
        header = slice(header, offset, len(header) - offset)
    assert slice(header, 0, 1) == b'\xa0', "Expected prevRandao to be a 32-byte string"
    return slice(header, 1, 32)

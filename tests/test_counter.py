import rlp
import pytest
import web3
from hexbytes import HexBytes

from contracts import RlpUtilsHarness

from tests.util import get_block_header

@pytest.fixture
def w3():
    return web3.Web3(web3.HTTPProvider('https://rpc.chiadochain.net'))

def test_blockhash_example(w3):
    block_number = 16967740
    block = w3.eth.get_block(block_number, full_transactions=False)

    header = get_block_header(w3, block_number)
    assert w3.keccak(rlp.encode(header)) == block['hash']

def test_rlp_expect_list(w3, rlp_utils_harness_contract):
    length, offset = rlp_utils_harness_contract.expect_list(HexBytes('0xc0'), 0)
    assert length == 0
    assert offset == 1
    length, offset = rlp_utils_harness_contract.expect_list(HexBytes('0xc180'), 0)
    assert length == 1
    assert offset == 1
    header = get_block_header(w3, 16967740)
    length, offset = rlp_utils_harness_contract.expect_list(rlp.encode(header), 0)
    assert length == sum(len(rlp.encode(el)) for el in header)
    assert offset == 3

def test_rlp_skip_string(w3, rlp_utils_harness_contract):
    offset = rlp_utils_harness_contract.skip_string(HexBytes('0x01'), 0)
    assert offset == 1
    offset = rlp_utils_harness_contract.skip_string(HexBytes('0x80'), 0)
    assert offset == 1
    offset = rlp_utils_harness_contract.skip_string(HexBytes('0x8180c0'), 0)
    assert offset == 2
    header = get_block_header(w3, 16967740)
    for i in range(len(header)):
        input = b"".join(rlp.encode(el) for el in header[i:])
        offset = rlp_utils_harness_contract.skip_string(input, 0)
        print(offset, rlp.encode(header[i]))
        assert offset == len(rlp.encode(header[i]))

def test_extract_prevrandao(w3, rlp_utils_harness_contract):
    block_number = 16967740
    header = get_block_header(w3, block_number)
    block = w3.eth.get_block(block_number, full_transactions=False)

    print(block['difficulty'])
    rlp_header = rlp.encode(header)
    prev_randao = rlp_utils_harness_contract.extract_prevrandao(rlp_header)
    assert prev_randao == block['mixHash']

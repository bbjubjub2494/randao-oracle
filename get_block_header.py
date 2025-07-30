import sys

import web3
import rlp

from moccasin.config import get_config

from tests.util import get_block_header

if len(sys.argv) != 3:
    print("Usage: uvx get_block_header.py <rpc_url> <block_number>")
    sys.exit(1)

rpc_url = sys.argv[1]
block_number = int(sys.argv[2])

w3 = web3.Web3(web3.HTTPProvider(rpc_url))

while w3.eth.block_number < block_number:
    time.sleep(1)

header = get_block_header(w3, block_number)
print("0x"+rlp.encode(header).hex())

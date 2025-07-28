from hexbytes import HexBytes

def get_block_header(w3, block_number):
    block = w3.eth.get_block(block_number, full_transactions=False)
    header = [
        block['parentHash'],
        block['sha3Uncles'],
        HexBytes(block['miner']),
        block['stateRoot'],
        block['transactionsRoot'],
        block['receiptsRoot'],
        block['logsBloom'],
        block['difficulty'],
        block['number'],
        block['gasLimit'],
        block['gasUsed'],
        block['timestamp'],
        block['extraData'],
        block['mixHash'],
        block['nonce'],
    ]
    if 'baseFeePerGas' in block:
        header.append(block['baseFeePerGas'])
    if 'withdrawalsRoot' in block:
        header.append(block['withdrawalsRoot'])
    if 'blobGasUsed' in block:
        header.append(block['blobGasUsed'])
        header.append(block['excessBlobGas'])
    if 'parentBeaconBlockRoot' in block:
        header.append(block['parentBeaconBlockRoot'])
    if 'requestsHash' in block:
        header.append(block['requestsHash'])

    return header

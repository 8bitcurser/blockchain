from json import dumps
from time import time

from block import Block, BlockChain
from flask import Flask, request
from helpers import consensus
from textract import process

app = Flask(__name__)

blockchain = BlockChain()


@app.route('/new_trans', methods=['POST'])
def new_trans():
    """Include a new unverified transaction to the chain."""
    tx_data = request.get_json()
    required_fields = ('author', 'content')

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404

    # Extract text content from PDF file.
    if '.pdf' in tx_data['file']:
        content = process(tx_data['file'])
        tx_data['content'] = content
    tx_data["timestamp"] = time()
    blockchain.add_new_transaction(tx_data)

    return "Success", 202


@app.route('/chain', methods=['GET'])
def get_chain():
    """Return blockchain after acquiring the longest."""
    consensus(request.host, blockchain, blockchain.peers)
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    ret = {
        "length": len(chain_data),
        "chain": chain_data
    }
    return dumps(ret)


@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    """Mine transactions to be appended to the blockchain as blocks"""
    result = blockchain.mine()
    if not result:
        ret = "No transactions to mine"
    else:
        ret = "Block #{} is mined.".format(result)
    return ret


# endpoint to query unconfirmed transactions
@app.route('/pending_tx')
def get_pending_tx():
    """Return all transactions that have not been mined yet."""
    return dumps(blockchain.unconfirmed_transactions)


# endpoint to add new peers to the network.
@app.route('/add_nodes', methods=['POST'])
def register_new_peers():
    """Register a new host to the pool of peers."""
    nodes = request.get_json()
    nodes = nodes['hosts']
    if not nodes:
        ret = "Invalid data", 400
    else:
        for node in nodes:
            blockchain.peers.add(node)
        ret = "Success", 201
    return ret


@app.route('/add_block', methods=['POST'])
def validate_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"], block_data["transactions"],
                  block_data["timestamp", block_data["previous_hash"]])
    proof = block_data['hash']
    added = blockchain.add_block(block, proof)
    if not added:
        ret, code = "The block was discarded by the node", 400
    else:
        ret, code = "Block added to the chain", 201

    return ret, code


if __name__ == "__main__":
    app.run(debug=True, port=8000)

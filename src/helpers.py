from requests import get


def consensus(host, blockchain, peers):
    """Consensus algorithm replace our chain for a longer one if exists.
    Arguments:
        host -- (str) our host url.
        blockchain -- (obj) blockchain instance.
        peers -- (set) collection of all the blockchain contributors.

    """
    longest_chain = None
    current_len = len(blockchain.chain)
    ret = True
    for node in peers:
        if node != host:
            response = get('http://{}/chain'.format(node))
            length = response.json()['length']
            chain = response.json()['chain']
            if length > current_len and blockchain.check_chain_validity(chain):
                current_len = length
                longest_chain = chain
        if longest_chain:
            blockchain = longest_chain
        else:
            ret = False
    return ret

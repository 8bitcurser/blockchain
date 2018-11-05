from hashlib import sha256
from json import dumps
from time import time
from requests import post


class Block:
    """Block abstraction class."""
    def __init__(self, index, transactions, timestamp, previous_hash):
        """Initialize block.
        Arguments:
            index -- (int) index of block element.
            transactions -- (list) list of pending transactions.
            timestamp -- (str) timestamp.
            previous_hash -- (str) hash of the previous block.
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash

    def compute_hash(self):
        """Hashes the block. Returns hex of sha256 hash.
        Arguments:
            self -- block class instance."""
        block_str = dumps(self.__dict__, sort_keys=True)
        return sha256(block_str.encode()).hexdigest()


class BlockChain:
    """Blockchain abstraction class that works with Block class."""
    # Dificulty of the Proof of work algorithim (PoW)
    pow_difficulty = 2
    peers = set()

    def __init__(self):
        """Initialization of class."""
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """This function creates the genesis block and adds it to the chain."""
        genesis_block = Block(0, [], time(), '0')
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def proof_of_work(self, block):
        """Function that returns only a hash that satisfies certain level of
           dificulty.
        Arguments:
            block -- Block class instance.
        """
        block.nonce = 2
        block_hash = block.compute_hash()
        while not block_hash.startswith('0' * self.pow_difficulty):
            block.nonce += 1
            block_hash = block.compute_hash()
        return block_hash

    def add_block(self, block, proof):
        """Add block to chain after validation.
        Arguments:
            block -- Block class instance.
            proof -- proof of work.
        """
        ret = False
        previous_hash = self.last_block.hash
        if previous_hash == block.previous_hash and \
                self.is_valid_proof(block, proof):
            block.hash = proof
            self.chain.append(block)
            ret = True
        return ret

    def is_valid_proof(self, block, block_hash):
        """Checks if block_hash is a valid hash.i
        Arguments:
            block -- Block class instance.
            block_hash -- (str) hash of the block."""
        begin = block_hash.startswith('0' * self.pow_difficulty)
        hash_identity = block_hash == block.compute_hash()
        return begin and hash_identity

    def add_new_transaction(self, transaction):
        """Add a new transaction to the unconfirmed list.
        Arguments:
            transaction -- (str) transaction
        """
        if transaction not in self.unconfirmed_transactions:
            self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """Add the pending transactions to the block, validate the PoW.
        Arguments:
            self -- (obj) blockchain object instance.
        """
        if self.unconfirmed_transactions:
            last_block = self.last_block
            new_block = Block(
                index=last_block.index+1,
                transactions=self.unconfirmed_transactions,
                timestamp=time(),
                previous_hash=last_block.hash
            )
            proof = self.proof_of_work(new_block)
            self.add_block(new_block, proof)
            self.unconfirmed_transactions = []
            self.announce_new_block(new_block)
            return new_block.index

    def announce_new_block(self, block):
        """Announce addition of a new block to all the peers.
        Arguments:
            self -- (obj) blockchain object instance.
            block -- (obj) block object instance.
        """
        for peer in self.peers:
            url = "http://{}/add_block".format(peer)
            post(url, data=dumps(block.__dict__, sort_keys=True))

    @property
    def last_block(self):
        """Return last block from the chain.
        Arguments:
            self -- (obj) blockchain object instance.
        """
        return self.chain[-1]

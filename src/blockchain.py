from urllib.parse import urlparse
from uuid import uuid4
from time import time
from hashlib import sha256
from collections import OrderedDict

import json

class Block(object):
    def __init__(self, index, transactions, timestamp, previous_hash, nonce):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def __call__(self):
        return self.__dict__

    def compute_hash(self):
        bstr = json.dumps(self(), sort_keys=True)
        return sha256(bstr.encode()).hexdigest()

class Transaction(object):
    def __init__(self, sender_address, signature, transaction):
        self.sender_address = sender_address
        self.signature = signature
        self.transaction = transaction

    def __call__(self):
        return OrderedDict(self.__dict__)

class Blockchain:

    def __init__(self):

        self.transactions = []
        self.chain = []
        self.nodes = set()
        self.node_id = str(uuid4()).replace("-","")
        self.create_block(0, "00")

    def register_node(self, node_url):
        parsed_url = urlparse(node_url)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError("Invalid url")

    def create_block(self, nonce, previous_hash):
        block = {"block_number": len(self.chain) +1,
                 "timestamp": time(),
                 "transactions": self.transactions,
                 "nonce": nonce,
                 "previous_hash": previous_hash}
        self.transactions = []
        self.chain.append(block)
        return block

if __name__ == "__main__":

    blockchain = Blockchain()
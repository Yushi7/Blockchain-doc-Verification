"""
Implements Block and Blockchain classes with:
  - SHA-256 hashing
  - Proof-of-Work consensus
  - Hash-chain linking
  - Tamper detection
"""

import hashlib
import json
import time


class Block:
    """
    A single block in the chain.

    Attributes:
    index       - Position in the chain (0 = genesis)
    timestamp   - Unix time of creation
    data        - Document metadata stored in this block
    prev_hash   - Hash of the previous block (links the chain)
    nonce       - Proof-of-work counter
    hash        - SHA-256 hash of this block's contents
    """

    def __init__(self, index: int, data: dict, prev_hash: str = "0"):
        self.index      = index
        self.timestamp  = time.time()
        self.data       = data          
        self.prev_hash  = prev_hash
        self.nonce      = 0
        self.hash       = self.compute_hash()

    def compute_hash(self) -> str:
        """Return the SHA-256 hash of this block's serialized contents."""
        block_string = json.dumps(
            {
                "index":     self.index,
                "timestamp": self.timestamp,
                "data":      self.data,
                "prev_hash": self.prev_hash,
                "nonce":     self.nonce,
            },
            sort_keys=True,
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "index":     self.index,
            "timestamp": self.timestamp,
            "data":      self.data,
            "prev_hash": self.prev_hash,
            "nonce":     self.nonce,
            "hash":      self.hash,
        }

    def __repr__(self):
        return (
            f"Block(index={self.index}, "
            f"hash={self.hash[:12]}..., "
            f"prev={self.prev_hash[:12]}...)"
        )


class Blockchain:
   # A tamper-evident chain of blocks secured by SHA-256 and proof-of-work.
   # difficulty - Number of leading zeros required in a valid block hash (Pow)

    DIFFICULTY = 3  

    def __init__(self):
        self.chain: list[Block] = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis = Block(index=0, data={"info": "Genesis Block"}, prev_hash="0")
        genesis.hash = self._proof_of_work(genesis)
        self.chain.append(genesis)

    def _proof_of_work(self, block: Block) -> str:
        """
        Increment nonce until the block hash starts with DIFFICULTY zeros.
        Returns the valid hash.
        """
        block.nonce = 0
        computed = block.compute_hash()
        while not computed.startswith("0" * self.DIFFICULTY):
            block.nonce += 1
            computed = block.compute_hash()
        return computed

    def add_block(self, data: dict) -> Block:
        prev_block = self.chain[-1]
        new_block  = Block(
            index     = len(self.chain),
            data      = data,
            prev_hash = prev_block.hash,
        )
        new_block.hash = self._proof_of_work(new_block)
        self.chain.append(new_block)
        return new_block

    def is_valid(self) -> bool:
        # Validate the entire chain
        # Returns True if the chain is intact, False if tampered
      
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # Check stored hash is still valid
            if curr.hash != curr.compute_hash():
                return False

            # Check chain linkage
            if curr.prev_hash != prev.hash:
                return False

            # Check proof-of-work
            if not curr.hash.startswith("0" * self.DIFFICULTY):
                return False

        return True

    def find_block_by_doc_id(self, doc_id: str):
        """Return the block containing the given document ID, or None."""
        for block in self.chain[1:]:   # skip genesis
            if block.data.get("doc_id") == doc_id:
                return block
        return None

    def print_chain(self):
        for block in self.chain:
            print(f"\n{'='*60}")
            print(f"  Block #{block.index}")
            print(f"  Timestamp : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))}")
            print(f"  Data      : {block.data}")
            print(f"  Nonce     : {block.nonce}")
            print(f"  Prev Hash : {block.prev_hash}")
            print(f"  Hash      : {block.hash}")
        print(f"{'='*60}\n")

    def __len__(self):
        return len(self.chain)

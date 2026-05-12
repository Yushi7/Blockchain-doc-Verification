"""
test_blockchain.py — Unit tests for blockchain and verification logic
Run: python -m pytest test_blockchain.py -v
"""

import pytest
import time
from blockchain import Blockchain, Block
from document import hash_text, build_document_record
from verify import simulate_tampering


# ── Block Tests ───────────────────────────────────────────────────────────────

class TestBlock:
    def test_hash_is_computed_on_init(self):
        block = Block(index=1, data={"test": "data"}, prev_hash="abc")
        assert block.hash is not None
        assert len(block.hash) == 64          # SHA-256 = 64 hex chars

    def test_hash_changes_when_nonce_changes(self):
        block = Block(index=1, data={"test": "data"}, prev_hash="abc")
        h1 = block.compute_hash()
        block.nonce += 1
        h2 = block.compute_hash()
        assert h1 != h2

    def test_to_dict_has_all_fields(self):
        block = Block(index=0, data={"info": "genesis"}, prev_hash="0")
        d = block.to_dict()
        assert all(k in d for k in ["index", "timestamp", "data", "prev_hash", "nonce", "hash"])


# ── Blockchain Tests ──────────────────────────────────────────────────────────

class TestBlockchain:
    def setup_method(self):
        self.chain = Blockchain()

    def test_genesis_block_exists(self):
        assert len(self.chain) == 1
        assert self.chain.chain[0].index == 0

    def test_genesis_prev_hash_is_zero(self):
        assert self.chain.chain[0].prev_hash == "0"

    def test_add_block_increases_chain_length(self):
        self.chain.add_block({"doc_id": "DOC-001", "doc_hash": "abc123"})
        assert len(self.chain) == 2

    def test_new_block_links_to_prev(self):
        self.chain.add_block({"doc_id": "DOC-001", "doc_hash": "abc"})
        self.chain.add_block({"doc_id": "DOC-002", "doc_hash": "def"})
        assert self.chain.chain[2].prev_hash == self.chain.chain[1].hash

    def test_chain_valid_after_adding_blocks(self):
        self.chain.add_block({"doc_id": "DOC-001", "doc_hash": "abc"})
        self.chain.add_block({"doc_id": "DOC-002", "doc_hash": "def"})
        assert self.chain.is_valid() is True

    def test_proof_of_work_meets_difficulty(self):
        block = self.chain.add_block({"doc_id": "DOC-001", "doc_hash": "xyz"})
        assert block.hash.startswith("0" * Blockchain.DIFFICULTY)

    def test_chain_invalid_after_data_tamper(self):
        self.chain.add_block({"doc_id": "DOC-001", "doc_hash": "legit_hash"})
        simulate_tampering(self.chain, 1, "tampered_hash")
        assert self.chain.is_valid() is False

    def test_chain_invalid_after_hash_tamper(self):
        self.chain.add_block({"doc_id": "DOC-001", "doc_hash": "legit_hash"})
        self.chain.chain[1].hash = "00000fakehash"
        assert self.chain.is_valid() is False

    def test_find_block_by_doc_id(self):
        self.chain.add_block({"doc_id": "DOC-001", "doc_hash": "h1"})
        self.chain.add_block({"doc_id": "DOC-002", "doc_hash": "h2"})
        block = self.chain.find_block_by_doc_id("DOC-002")
        assert block is not None
        assert block.data["doc_id"] == "DOC-002"

    def test_find_block_returns_none_for_missing(self):
        result = self.chain.find_block_by_doc_id("NONEXISTENT")
        assert result is None


# ── Document Record Tests ─────────────────────────────────────────────────────

class TestDocument:
    def test_hash_text_returns_64_char_hex(self):
        h = hash_text("hello world")
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)

    def test_same_content_same_hash(self):
        assert hash_text("document content") == hash_text("document content")

    def test_different_content_different_hash(self):
        assert hash_text("original") != hash_text("modified")

    def test_build_document_record_keys(self):
        record = build_document_record("DOC-001", "abc123", "Ayushi", "file.pdf")
        assert all(k in record for k in ["doc_id", "doc_hash", "owner", "filename", "issued_at"])

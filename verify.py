"""
verify.py — Document verification against the blockchain
"""

from blockchain import Blockchain
from document import hash_document, hash_text


def register_document(chain: Blockchain, doc_id: str, filepath: str, owner: str) -> dict:
    """
    Hash a document file and register it as a new block on the chain.

    Returns the block data dict on success.
    Raises FileNotFoundError if the file does not exist.
    """
    import os
    doc_hash = hash_document(filepath)
    filename = os.path.basename(filepath)

    data = {
        "doc_id":   doc_id,
        "doc_hash": doc_hash,
        "owner":    owner,
        "filename": filename,
    }

    block = chain.add_block(data)
    print(f"[✔] Document registered in Block #{block.index}")
    print(f"    Doc ID  : {doc_id}")
    print(f"    Hash    : {doc_hash}")
    return data


def verify_document(chain: Blockchain, doc_id: str, filepath: str) -> bool:
    """
    Verify a document against its registered hash on the blockchain.

    Steps
    -----
    1. Look up the block containing doc_id.
    2. Recompute the file's SHA-256 hash.
    3. Compare against the stored hash.
    4. Also validate that the overall chain is intact.

    Returns True if document is authentic and chain is valid.
    """
    # Step 1: find the block
    block = chain.find_block_by_doc_id(doc_id)
    if not block:
        print(f"[✘] Document ID '{doc_id}' not found on the blockchain.")
        return False

    # Step 2: recompute current file hash
    try:
        current_hash = hash_document(filepath)
    except FileNotFoundError:
        print(f"[✘] File not found: {filepath}")
        return False

    # Step 3: compare hashes
    stored_hash = block.data.get("doc_hash")
    hashes_match = current_hash == stored_hash

    # Step 4: validate chain integrity
    chain_valid = chain.is_valid()

    print(f"\n{'='*55}")
    print(f"  Verification Report — {doc_id}")
    print(f"{'='*55}")
    print(f"  File          : {filepath}")
    print(f"  Stored Hash   : {stored_hash}")
    print(f"  Current Hash  : {current_hash}")
    print(f"  Hash Match    : {'✔ YES' if hashes_match else '✘ NO — FILE TAMPERED'}")
    print(f"  Chain Intact  : {'✔ YES' if chain_valid else '✘ NO — CHAIN TAMPERED'}")
    print(f"{'='*55}\n")

    return hashes_match and chain_valid


def simulate_tampering(chain: Blockchain, block_index: int, new_value: str):
    """
    Directly mutate a block's stored data to demonstrate tamper detection.
    After this call, chain.is_valid() should return False.
    """
    if block_index >= len(chain.chain):
        print("Block index out of range.")
        return
    chain.chain[block_index].data["doc_hash"] = new_value
    print(f"[!] Block #{block_index} data has been tampered with.")
    print(f"    chain.is_valid() → {chain.is_valid()}")

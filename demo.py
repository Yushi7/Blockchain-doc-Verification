# demo.py — Demonstrates the full blockchain verification workflow without needing real files

import time
from blockchain import Blockchain
from document import hash_text, build_document_record
from verify import simulate_tampering


def main():
    print("\n" + "=" * 60)
    print("   DEMO: Blockchain Document Verification System")
    print("=" * 60)

    chain = Blockchain()
    print(f"\n[1] Genesis block created. Chain length: {len(chain)}")

    documents = [
        ("DOC-001", "Ayushi_Degree_Certificate.pdf", "Ayushi Nishita Ekka"),
        ("DOC-002", "Internship_Offer_Letter.pdf",   "HR Team"),
        ("DOC-003", "Marksheet_Sem3.pdf",             "BIT Mesra"),
    ]

    print("\n[2] Registering documents on the blockchain ...\n")
    for doc_id, filename, owner in documents:
        # replace hash_text with hash_document for real files
        fake_content = f"{doc_id}|{filename}|{owner}|simulated"
        doc_hash = hash_text(fake_content)

        data = build_document_record(doc_id, doc_hash, owner, filename)
        block = chain.add_block(data)
        print(f"  {doc_id} registered -> Block #{block.index}  |  Hash: {block.hash[:20]}...")
        time.sleep(0.1)

    print("\n[3] Full blockchain:")
    chain.print_chain()

    print("[4] Chain integrity check:", "VALID" if chain.is_valid() else "INVALID")

    # ── Verify a known-good document ─────────────────────────────────────────
    print("\n[5] Verifying DOC-001 (unmodified) ...")
    block = chain.find_block_by_doc_id("DOC-001")
    stored_hash  = block.data["doc_hash"]
    current_hash = hash_text("DOC-001|Ayushi_Degree_Certificate.pdf|Ayushi Nishita Ekka|simulated")
    match = stored_hash == current_hash
    print(f"  Stored Hash  : {stored_hash}")
    print(f"  Current Hash : {current_hash}")
    print(f"  Result       : {'AUTHENTIC' if match else 'TAMPERED'}")

    # ── Simulate tampering ────────────────────────────────────────────────────
    print("\n[6] Simulating document tampering on Block #1 ...")
    simulate_tampering(chain, 1, "deadbeef" * 8)

    print("\n[7] Re-checking chain integrity after tampering:")
    print("  Chain valid:", "VALID" if chain.is_valid() else "INVALID — TAMPERING DETECTED")

    print("\n" + "=" * 60)
    print("  Demo complete.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

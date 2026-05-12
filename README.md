# Blockchain-Based Document Verification System

A tamper-proof document verification system built in **Python** using a custom blockchain with **SHA-256 hashing** and **Proof-of-Work consensus**. Any alteration to a registered document is instantly detectable through hash-chain verification.

---

## How It Works

```
Document File
     │
     ▼
SHA-256 Hash  ──────────────────────────────────────────────────────┐
                                                                     │
                   ┌──────────────┐     ┌──────────────┐            │
  Genesis Block ──▶│   Block #1   │────▶│   Block #2   │────▶  ...  │
                   │  doc_id      │     │  doc_id      │            │
                   │  doc_hash ◀──┼─────┼──────────────┼────────────┘
                   │  owner       │     │  owner       │
                   │  prev_hash   │     │  prev_hash   │
                   │  nonce (PoW) │     │  nonce (PoW) │
                   └──────────────┘     └──────────────┘

To verify: recompute file hash → compare with stored hash → validate chain
```

**Tamper detection:** If a document is altered after registration, its recomputed hash will not match the stored hash. If a block itself is altered, the hash-chain linkage breaks and `is_valid()` returns `False`.

---

## Features

- **SHA-256 document hashing** — unique fingerprint for every file
- **Hash-chain linking** — each block stores the hash of the previous block
- **Proof-of-Work** — mining ensures computational cost to add blocks
- **Tamper detection** — any modification to data or hashes is caught instantly
- **CLI interface** — register, verify, and inspect documents interactively
- **Demo script** — runs the full workflow without real files
- **Unit tests** — 15 tests covering blockchain integrity and document logic

---

## Project Structure

```
blockchain-doc-verification/
├── blockchain.py        # Block & Blockchain classes (SHA-256, PoW, validation)
├── document.py          # Document hashing & metadata utilities
├── verify.py            # Register and verify documents against the chain
├── main.py              # Interactive CLI
├── demo.py              # Full demo without real files
├── test_blockchain.py   # Unit tests (pytest)
├── requirements.txt
└── README.md
```

---

## Setup & Installation

**Prerequisites:** Python 3.8+ (no external libraries needed for core functionality)

```bash
# Clone the repo
git clone https://github.com/Yushi7/blockchain-doc-verification.git
cd blockchain-doc-verification

# Install test dependency (optional)
pip install -r requirements.txt

# Run the demo
python demo.py

# Run the interactive CLI
python main.py

# Run tests
python -m pytest test_blockchain.py -v
```

---

## Demo Output

```
============================================================
   DEMO: Blockchain Document Verification System
============================================================

[1] Genesis block created. Chain length: 1

[2] Registering documents on the blockchain 
   DOC-001 registered → Block #1  |  Hash: 000a3f9b1c2e47...
   DOC-002 registered → Block #2  |  Hash: 0007d8f2a1b34c...
   DOC-003 registered → Block #3  |  Hash: 000e2a7c9f1d58...

[4] Chain integrity check: VALID

[5] Verifying DOC-001 (unmodified) 
  Result: AUTHENTIC

[6] Simulating document tampering on Block #1 
[!] Block #1 data has been tampered with.

[7] Re-checking chain integrity after tampering:
  Chain valid: INVALID — TAMPERING DETECTED
```

---

## Core Concepts

### SHA-256 Hashing
Every document is reduced to a unique 256-bit fingerprint. Even a single character change in the file produces a completely different hash (avalanche effect).

### Hash-Chain Linking
Each block stores the hash of the previous block in its `prev_hash` field. This creates a cryptographic chain — altering any block invalidates all subsequent blocks.

### Proof of Work
Before a block can be added, the system increments a `nonce` until the block's hash starts with `DIFFICULTY` leading zeros. This makes retroactive tampering computationally expensive.

### Verification Flow
```
1. Look up block by doc_id
2. Recompute SHA-256 hash of current file
3. Compare with hash stored in block
4. Also run chain.is_valid() to check chain integrity
5. Both must pass for the document to be certified authentic
```

---

## Technologies Used

| Component         | Technology           |
|-------------------|----------------------|
| Language          | Python 3             |
| Hashing           | SHA-256 (hashlib)    |
| Consensus         | Proof-of-Work        |
| Serialization     | JSON                 |
| Testing           | pytest               |

---


"""
main.py — CLI interface for the Blockchain Document Verification System
"""

import os
from blockchain import Blockchain
from verify import register_document, verify_document, simulate_tampering

# Global chain instance (in a real app, persist this to disk/DB)
chain = Blockchain()


def menu():
    while True:
        print("\n" + "=" * 50)
        print("   Blockchain Document Verification System")
        print("=" * 50)
        print("1. Register a Document")
        print("2. Verify a Document")
        print("3. View Full Blockchain")
        print("4. Check Chain Integrity")
        print("5. Simulate Tampering (Demo)")
        print("6. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            doc_id   = input("Document ID (e.g. DOC-001): ").strip()
            filepath = input("File path: ").strip()
            owner    = input("Owner name: ").strip()
            if not os.path.exists(filepath):
                print(f"[✘] File '{filepath}' does not exist.")
            else:
                register_document(chain, doc_id, filepath, owner)

        elif choice == "2":
            doc_id   = input("Document ID to verify: ").strip()
            filepath = input("File path: ").strip()
            result   = verify_document(chain, doc_id, filepath)
            if result:
                print("✔ Document is AUTHENTIC.")
            else:
                print("✘ Document verification FAILED.")

        elif choice == "3":
            chain.print_chain()

        elif choice == "4":
            valid = chain.is_valid()
            print(f"\nChain integrity: {'✔ VALID' if valid else '✘ INVALID — CHAIN HAS BEEN TAMPERED'}")

        elif choice == "5":
            print("\n[Demo] Simulating tampering on Block #1 ...")
            if len(chain) < 2:
                print("Register at least one document first.")
            else:
                simulate_tampering(chain, 1, "0000000000000000000000000000000000000000000000000000000000000000")

        elif choice == "6":
            print("Exiting.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()

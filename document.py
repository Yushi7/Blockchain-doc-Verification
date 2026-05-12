"""
document.py — Document hashing and metadata utilities
"""

import hashlib
import os
import time


def hash_document(filepath: str) -> str:
    """
    Compute the SHA-256 hash of a file's contents.
    Reads in chunks to handle large files efficiently.

    Parameters
    ----------
    filepath : Path to the document file

    Returns
    -------
    Hex-encoded SHA-256 digest string
    """
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        raise FileNotFoundError(f"Document not found: {filepath}")


def hash_text(content: str) -> str:
    """Compute SHA-256 hash of a plain text string (for demo/testing)."""
    return hashlib.sha256(content.encode()).hexdigest()


def build_document_record(doc_id: str, doc_hash: str, owner: str, filename: str) -> dict:
    """
    Build the data payload to be stored inside a block.

    Parameters
    ----------
    doc_id   : Unique identifier for the document (e.g. 'DOC-001')
    doc_hash : SHA-256 hash of the document file
    owner    : Name or ID of the person registering the document
    filename : Original filename

    Returns
    -------
    Dict to be stored in the block's data field
    """
    return {
        "doc_id":    doc_id,
        "doc_hash":  doc_hash,
        "owner":     owner,
        "filename":  filename,
        "issued_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

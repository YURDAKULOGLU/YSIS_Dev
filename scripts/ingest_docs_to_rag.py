#!/usr/bin/env python3
"""
Ingest vendor/framework documentation from platform_data into the vector store.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


def _iter_doc_files(root: Path) -> Iterable[Path]:
    exts = {".md", ".txt", ".rst"}
    ignore_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv"}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in exts:
            continue
        if any(part in ignore_dirs for part in path.parts):
            continue
        yield path


def _chunk_text(text: str, max_chars: int) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current: list[str] = []
    size = 0
    for paragraph in paragraphs:
        add_len = len(paragraph) + 2
        if current and size + add_len > max_chars:
            chunks.append("\n\n".join(current))
            current = [paragraph]
            size = len(paragraph)
        else:
            current.append(paragraph)
            size += add_len
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def _load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def ingest_docs(root: Path, collection: str, max_chars: int) -> int:
    from ybis.data_plane.vector_store import VectorStore

    vector_store = VectorStore()
    docs: list[str] = []
    metadata: list[dict] = []
    total = 0

    for doc_path in _iter_doc_files(root):
        text = _load_text(doc_path)
        for chunk in _chunk_text(text, max_chars=max_chars):
            docs.append(chunk)
            metadata.append(
                {
                    "source": str(doc_path),
                    "root": str(root),
                }
            )
            if len(docs) >= 50:
                vector_store.add_documents(collection, docs, metadata)
                total += len(docs)
                docs = []
                metadata = []

    if docs:
        vector_store.add_documents(collection, docs, metadata)
        total += len(docs)

    return total


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest docs into RAG store.")
    parser.add_argument(
        "--frameworks",
        action="store_true",
        help="Ingest platform_data/knowledge/Frameworks",
    )
    parser.add_argument(
        "--vendors",
        action="store_true",
        help="Ingest platform_data/knowledge/Vendors",
    )
    parser.add_argument(
        "--rules",
        action="store_true",
        help="Ingest platform_data/knowledge/Rules",
    )
    parser.add_argument(
        "--collection",
        default="knowledge",
        help="Vector store collection name (default: knowledge)",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=1200,
        help="Max chars per chunk (default: 1200)",
    )

    args = parser.parse_args()
    if not args.frameworks and not args.vendors and not args.rules:
        args.frameworks = True
        args.vendors = True
        args.rules = True

    roots = []
    if args.frameworks:
        roots.append(PROJECT_ROOT / "platform_data" / "knowledge" / "Frameworks")
    if args.vendors:
        roots.append(PROJECT_ROOT / "platform_data" / "knowledge" / "Vendors")
    if args.rules:
        roots.append(PROJECT_ROOT / "platform_data" / "knowledge" / "Rules")

    total = 0
    for root in roots:
        if not root.exists():
            print(f"[SKIP] {root} not found")
            continue
        try:
            count = ingest_docs(root, args.collection, args.max_chars)
            total += count
            print(f"[OK] Ingested {count} chunks from {root}")
        except ImportError as exc:
            print(f"[ERROR] Vector store unavailable: {exc}")
            return 1
        except Exception as exc:
            print(f"[ERROR] Failed to ingest {root}: {exc}")
            return 1

    print(f"[DONE] Total chunks ingested: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Doc Graph Builder - generates document link graph from docs/.
Outputs:
- docs/reports/doc_graph.json
- docs/reports/doc_graph.md
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

PROJECT_ROOT = Path(__file__).parent.parent
DOCS_ROOT = PROJECT_ROOT / "docs"
REPORTS_DIR = DOCS_ROOT / "reports"

LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+\.md[^)]*)\)")
INLINE_PATH_PATTERN = re.compile(r"`([^`]+\.md)`|(^|\s)(docs[/\\\\][^\\s]+\.md)", re.M)
REFERENCE_HEADER_PATTERN = re.compile(r"^References:\s*$", re.IGNORECASE)
FENCED_CODE_PATTERN = re.compile(r"```.*?```", re.S)
IGNORE_TARGET_PATTERNS = [
    re.compile(r"<[^>]+>"),  # placeholders like <task_id>
    re.compile(r"ADR-YYYYMMDD-<title>", re.IGNORECASE),
    re.compile(r"\*"),  # glob placeholders
    re.compile(r"\[[^\]]+\]"),  # template placeholders like [agent]
    re.compile(r"docs[/\\\\]reports[/\\\\]doc_graph.md", re.IGNORECASE),
    re.compile(r"docs[/\\\\]Güncel", re.IGNORECASE),
    re.compile(r"docs[/\\\\]governance[/\\\\]10_META[/\\\\]Güncel", re.IGNORECASE),
    re.compile(r"docs[/\\\\]governance[/\\\\]00_GENESIS[/\\\\]\\.YBIS_Dev", re.IGNORECASE),
    re.compile(r"docs[/\\\\]governance[/\\\\]00_GENESIS[/\\\\]\\.claude", re.IGNORECASE),
    re.compile(r"docs[/\\\\]governance[/\\\\]00_GENESIS[/\\\\]Veriler", re.IGNORECASE),
    re.compile(r"docs[/\\\\]governance[/\\\\]10_META[/\\\\]Archive", re.IGNORECASE),
    re.compile(r"docs[/\\\\]governance[/\\\\]10_META[/\\\\]Strategy[/\\\\]Meta", re.IGNORECASE),
    re.compile(r"docs[/\\\\]governance[/\\\\]10_META[/\\\\]Governance[/\\\\]10_META", re.IGNORECASE),
]
IGNORE_DOC_PATHS = [
    DOCS_ROOT / "reports",
]


@dataclass(frozen=True)
class DocNode:
    path: str
    title: str


@dataclass(frozen=True)
class DocEdge:
    source: str
    target: str
    kind: str


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text

    lines = text.splitlines()
    if len(lines) < 3:
        return {}, text

    try:
        end_index = lines[1:].index("---") + 1
    except ValueError:
        return {}, text

    frontmatter_text = "\n".join(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :])
    try:
        data = yaml.safe_load(frontmatter_text) or {}
    except Exception:
        data = {}
    return data, body


def _extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _strip_code_blocks(text: str) -> str:
    return re.sub(FENCED_CODE_PATTERN, "", text)


def _extract_reference_section(text: str) -> list[str]:
    lines = text.splitlines()
    refs: list[str] = []
    in_refs = False
    for line in lines:
        if REFERENCE_HEADER_PATTERN.match(line.strip()):
            in_refs = True
            continue
        if in_refs:
            if not line.strip():
                break
            match = re.findall(r"`([^`]+)`|\(([^)]+)\)", line)
            for group in match:
                candidate = group[0] or group[1]
                if candidate.endswith(".md"):
                    refs.append(candidate)
    return refs


def _extract_links(text: str) -> list[str]:
    cleaned = _strip_code_blocks(text)
    links = [match for match in LINK_PATTERN.findall(cleaned)]
    for match in INLINE_PATH_PATTERN.findall(cleaned):
        for candidate in match:
            if candidate and candidate.endswith(".md"):
                links.append(candidate)
    return links


def _normalize_path(raw: str, source: Path) -> Path | None:
    if not raw:
        return None
    candidate = raw.split("#", 1)[0].strip()
    if not candidate or candidate.startswith("http"):
        return None
    if candidate.startswith("docs/") or candidate.startswith("docs\\"):
        path = PROJECT_ROOT / candidate
    else:
        path = (source.parent / candidate).resolve()
    try:
        return path.relative_to(PROJECT_ROOT)
    except ValueError:
        return None


def _gather_docs() -> Iterable[Path]:
    if not DOCS_ROOT.exists():
        return []
    docs = []
    for path in DOCS_ROOT.rglob("*.md"):
        if any(parent in path.parents for parent in IGNORE_DOC_PATHS):
            continue
        docs.append(path)
    extra = [PROJECT_ROOT / "AGENTS.md"]
    return [*docs, *[p for p in extra if p.exists()]]


def build_graph() -> tuple[
    list[DocNode], list[DocEdge], list[dict[str, str]], list[dict[str, str]]
]:
    nodes: list[DocNode] = []
    edges: list[DocEdge] = []
    missing: list[dict[str, str]] = []
    ignored: list[dict[str, str]] = []

    docs = list(_gather_docs())
    doc_set = {doc.resolve() for doc in docs}

    for doc_path in docs:
        text = _load_text(doc_path)
        frontmatter, body = _split_frontmatter(text)
        title = _extract_title(body, doc_path.stem)
        nodes.append(DocNode(path=str(doc_path.relative_to(PROJECT_ROOT)), title=title))

        refs = []
        frontmatter_refs = frontmatter.get("references", [])
        if isinstance(frontmatter_refs, str):
            refs.append(frontmatter_refs)
        elif isinstance(frontmatter_refs, list):
            refs.extend(frontmatter_refs)

        refs.extend(_extract_reference_section(body))
        refs.extend(_extract_links(body))

        for ref in refs:
            if any(pattern.search(ref) for pattern in IGNORE_TARGET_PATTERNS):
                ignored.append(
                    {
                        "source": str(doc_path.relative_to(PROJECT_ROOT)),
                        "target": ref,
                        "reason": "ignored_pattern",
                    }
                )
                continue
            target_path = _normalize_path(ref, doc_path)
            if not target_path:
                continue
            abs_target = (PROJECT_ROOT / target_path).resolve()
            if abs_target in doc_set:
                edges.append(
                    DocEdge(
                        source=str(doc_path.relative_to(PROJECT_ROOT)),
                        target=str(target_path),
                        kind="reference",
                    )
                )
            else:
                missing.append(
                    {
                        "source": str(doc_path.relative_to(PROJECT_ROOT)),
                        "target": str(target_path),
                    }
                )

    return nodes, edges, missing, ignored


def _summarize(
    nodes: list[DocNode], edges: list[DocEdge], ignored: list[dict[str, str]]
) -> dict[str, Any]:
    inbound: dict[str, int] = {node.path: 0 for node in nodes}
    outbound: dict[str, int] = {node.path: 0 for node in nodes}
    for edge in edges:
        outbound[edge.source] = outbound.get(edge.source, 0) + 1
        inbound[edge.target] = inbound.get(edge.target, 0) + 1

    orphans = [path for path in inbound if inbound[path] == 0 and outbound[path] == 0]
    top_inbound = sorted(inbound.items(), key=lambda item: item[1], reverse=True)[:10]
    return {
        "total_docs": len(nodes),
        "total_edges": len(edges),
        "ignored_references": len(ignored),
        "orphans": orphans,
        "top_inbound": top_inbound,
    }


def write_outputs(
    nodes: list[DocNode],
    edges: list[DocEdge],
    missing: list[dict[str, str]],
    ignored: list[dict[str, str]],
) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()

    summary = _summarize(nodes, edges, ignored)

    json_payload = {
        "generated_at": generated_at,
        "nodes": [node.__dict__ for node in nodes],
        "edges": [edge.__dict__ for edge in edges],
        "missing_references": missing,
        "ignored_references": ignored,
        "summary": summary,
    }
    (REPORTS_DIR / "doc_graph.json").write_text(json.dumps(json_payload, indent=2), encoding="utf-8")

    lines = [
        "# Documentation Graph Report",
        "",
        f"**Generated:** {generated_at}",
        "",
        "## Summary",
        f"- **Total docs:** {summary['total_docs']}",
        f"- **Total edges:** {summary['total_edges']}",
        f"- **Orphans:** {len(summary['orphans'])}",
        f"- **Ignored references:** {summary['ignored_references']}",
        "",
        "## Top Referenced Docs",
    ]

    for doc, count in summary["top_inbound"]:
        lines.append(f"- {doc} ({count})")

    if summary["orphans"]:
        lines.extend(["", "## Orphan Docs"])
        for doc in summary["orphans"]:
            lines.append(f"- {doc}")

    if missing:
        lines.extend(["", "## Missing References"])
        for entry in missing[:50]:
            lines.append(f"- {entry['source']} -> {entry['target']}")
        if len(missing) > 50:
            lines.append(f"- ... and {len(missing) - 50} more")

    if ignored:
        lines.extend(["", "## Ignored References"])
        for entry in ignored[:20]:
            lines.append(f"- {entry['source']} -> {entry['target']} ({entry['reason']})")
        if len(ignored) > 20:
            lines.append(f"- ... and {len(ignored) - 20} more")

    (REPORTS_DIR / "doc_graph.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate doc graph reports.")
    parser.add_argument(
        "--fail-on-missing",
        action="store_true",
        help="Exit with failure if missing references are detected.",
    )
    parser.add_argument(
        "--max-missing",
        type=int,
        default=None,
        help="Allow up to this many missing references before failing.",
    )
    args = parser.parse_args()

    nodes, edges, missing, ignored = build_graph()
    write_outputs(nodes, edges, missing, ignored)
    print(f"[OK] Doc graph generated with {len(nodes)} docs and {len(edges)} edges.")
    if missing:
        print(f"[WARN] {len(missing)} missing doc references detected.")
        if args.fail_on_missing:
            if args.max_missing is None or len(missing) > args.max_missing:
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import shutil
from pathlib import Path

def _copy_docs_from_dir(source_dir: Path, target_dir: Path) -> int:
    """Copy common documentation files/folders from a repo into a KB folder."""
    copied = 0
    extensions = [".md", ".txt", ".rst"]
    target_dir.mkdir(parents=True, exist_ok=True)

    for item in source_dir.iterdir():
        if item.is_file() and any(item.name.lower().endswith(ext) for ext in extensions):
            shutil.copy(item, target_dir / item.name)
            copied += 1

    docs_folder = source_dir / "docs"
    if docs_folder.exists() and docs_folder.is_dir():
        shutil.copytree(docs_folder, target_dir / "docs", dirs_exist_ok=True)
        copied += 1

    return copied


def ingest_docs():
    tools_root = Path("tools")
    vendors_root = Path("vendors")
    kb_root = Path("platform_data/knowledge")
    frameworks_root = kb_root / "Frameworks"
    vendors_root_kb = kb_root / "Vendors"

    # 1. Process Frameworks from tools/ (legacy compatibility)
    if tools_root.exists():
        for tool_dir in tools_root.iterdir():
            if tool_dir.is_dir():
                target_kb = frameworks_root / tool_dir.name
                copied = _copy_docs_from_dir(tool_dir, target_kb)
                if copied:
                    print(f"[INGESTED] tools/{tool_dir.name} docs to KB.")

    # 2. Process Vendors from vendors/
    if vendors_root.exists():
        for vendor_dir in vendors_root.iterdir():
            if vendor_dir.is_dir():
                target_kb = vendors_root_kb / vendor_dir.name
                copied = _copy_docs_from_dir(vendor_dir, target_kb)
                if copied:
                    print(f"[INGESTED] vendors/{vendor_dir.name} docs to KB.")

    # 2. Process Libraries (Create summary docs for new pip installs)
    libs = {
        "LlamaIndex": "https://docs.llamaindex.ai/",
        "Ragas": "https://docs.ragas.io/",
        "PydanticAI": "https://ai.pydantic.dev/",
        "Guidance": "https://github.com/guidance-ai/guidance",
        "Unstructured": "https://unstructured-io.github.io/unstructured/",
        "OpenTelemetry": "https://opentelemetry.io/docs/"
    }
    
    for lib, url in libs.items():
        lib_kb = frameworks_root / lib
        lib_kb.mkdir(parents=True, exist_ok=True)
        with open(lib_kb / "source_link.txt", "w") as f:
            f.write(f"Official Docs: {url}")

if __name__ == "__main__":
    ingest_docs()

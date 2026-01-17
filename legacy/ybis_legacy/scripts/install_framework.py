#!/usr/bin/env python3
"""
Framework Installer with Automatic Documentation Download
Installs framework and automatically downloads all documentation to RAG.

⚠️  DEPRECATED: Use auto_scrape_package_docs.py instead for better features.
This script is kept for backward compatibility and framework installation only.
"""

import subprocess
import sys
import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import markdownify
from urllib.parse import urljoin, urlparse
import json

# Framework documentation URLs
FRAMEWORK_DOCS = {
    "aider": "https://aider.chat/docs/",  # Official Aider documentation
    "langgraph": "https://langchain-ai.github.io/langgraph/",
    "litellm": "https://docs.litellm.ai/",
    "redis": "https://redis.io/docs/",
    "crewai": "https://docs.crewai.com/",
    "autogen": "https://microsoft.github.io/autogen/",
    "ollama": "https://ollama.ai/docs/",
    "instructor": "https://github.com/jxnl/instructor",  # GitHub-based
    "swarm": None,  # Check GitHub
    "autogpt": None,  # Check GitHub
    "temporalio": "https://docs.temporal.io/",
    "ray": "https://docs.ray.io/",
    "prefect": "https://docs.prefect.io/",
    "spade": "https://spadeagents.eu/docs/",
    "celery": "https://docs.celeryproject.org/",
}


class FrameworkInstaller:
    """Install framework and download all documentation."""
    
    def __init__(self, framework_name: str):
        self.framework_name = framework_name.lower()
        self.docs_dir = Path(f"Knowledge/Frameworks/{self.framework_name}/docs")
        self.docs_dir.mkdir(parents=True, exist_ok=True)
    
    def install(self):
        """Install framework and download docs."""
        print(f"[INSTALL] Installing {self.framework_name}...")
        
        # 1. Install via pip
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", self.framework_name],
                check=True,
                capture_output=True
            )
            print(f"[OK] {self.framework_name} installed")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Installation failed: {e}")
            return False
        
        # 2. Download documentation
        print(f"[DOWNLOAD] Downloading documentation for {self.framework_name}...")
        self.download_docs()
        
        # 3. Ingest into RAG (if RAG available)
        print(f"[RAG] Ingesting docs into RAG...")
        self.ingest_to_rag()
        
        print(f"[SUCCESS] {self.framework_name} installed with full documentation!")
        return True
    
    def download_docs(self):
        """Download all documentation."""
        if self.framework_name in FRAMEWORK_DOCS:
            docs_url = FRAMEWORK_DOCS[self.framework_name]
            if docs_url and docs_url.startswith("http"):
                self._scrape_docs_site(docs_url)
            elif docs_url and "github.com" in docs_url:
                self._download_github_docs(docs_url)
            else:
                self._download_github_docs(f"https://github.com/{self.framework_name}/{self.framework_name}")
        else:
            # Try GitHub
            self._download_github_docs(f"https://github.com/{self.framework_name}/{self.framework_name}")
    
    def _scrape_docs_site(self, base_url: str):
        """Scrape documentation site and convert to markdown."""
        print(f"  Scraping {base_url}...")
        
        try:
            # Get main page
            response = requests.get(base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all documentation links
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                if self._is_doc_page(full_url, base_url):
                    links.append(full_url)
            
            # Download each page (deduplicate links first)
            unique_links = list(set(links))[:50]  # Limit to 50 pages
            for i, url in enumerate(unique_links, 1):
                try:
                    print(f"  [{i}/{len(unique_links)}] Downloading {url}...")
                    page_response = requests.get(url, timeout=10)
                    page_soup = BeautifulSoup(page_response.content, 'html.parser')
                    
                    # Extract content
                    content = page_soup.find('main') or page_soup.find('article') or page_soup.find('body')
                    if content:
                        # Convert to markdown
                        markdown_content = markdownify.markdownify(str(content), heading_style="ATX")
                        
                        # Save
                        filename = self._url_to_filename(url)
                        filepath = self.docs_dir / filename
                        filepath.write_text(markdown_content, encoding='utf-8')
                except Exception as e:
                    print(f"    [WARN] Failed to download {url}: {e}")
                    continue
                    
        except Exception as e:
            print(f"  [WARN] Failed to scrape docs: {e}")
            # Fallback to GitHub
            self._download_github_docs(None)  # Will use repo_mappings
    
    def _download_github_docs(self, repo_url: str = None):
        """Download documentation from GitHub repo."""
        # Framework-specific repo mappings
        repo_mappings = {
            "prefect": ("prefecthq", "prefect"),
            "spade": ("javipalanca", "spade"),
            "celery": ("celery", "celery"),
            "temporalio": ("temporalio", "python-sdk"),
            "ray": ("ray-project", "ray"),
            "pyautogen": ("microsoft", "autogen"),
            "autogen": ("microsoft", "autogen"),
            "swarm": ("swarm-ai", "swarm"),  # Example, verify actual repo
            "autogpt": ("Significant-Gravitas", "AutoGPT"),
            "langgraph": ("langchain-ai", "langgraph"),
            "litellm": ("BerriAI", "litellm"),
            "instructor": ("jxnl", "instructor"),
            "ollama": ("ollama", "ollama"),
        }
        
        try:
            # Try framework-specific mapping first
            if self.framework_name in repo_mappings:
                owner, repo = repo_mappings[self.framework_name]
                print(f"  Downloading from GitHub: https://github.com/{owner}/{repo}...")
            elif repo_url and "github.com" in repo_url:
                print(f"  Downloading from GitHub: {repo_url}...")
                # Extract owner/repo from URL
                parts = repo_url.replace("https://github.com/", "").split("/")
                if len(parts) >= 2:
                    owner, repo = parts[0], parts[1]
                else:
                    print(f"    [WARN] Could not parse GitHub URL: {repo_url}")
                    return
            else:
                print(f"    [WARN] Not a GitHub URL: {repo_url}")
                return
            
            # Download README
            for branch in ["main", "master", "develop"]:
                readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
                try:
                    readme_response = requests.get(readme_url, timeout=10)
                    if readme_response.status_code == 200:
                        (self.docs_dir / "README.md").write_text(readme_response.text, encoding='utf-8')
                        print(f"    [OK] README.md downloaded from {branch} branch")
                        break
                except:
                    continue
            
            # Try docs/ folder (recursive)
            self._download_github_docs_recursive(owner, repo, "docs", self.docs_dir)
                    
        except Exception as e:
            print(f"    [WARN] GitHub download failed: {e}")
    
    def _download_github_docs_recursive(self, owner: str, repo: str, path: str, target_dir: Path, max_depth: int = 3, current_depth: int = 0):
        """Recursively download docs from GitHub."""
        if current_depth >= max_depth:
            return
        
        try:
            docs_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
            docs_response = requests.get(docs_url, timeout=10)
            if docs_response.status_code == 200:
                items = docs_response.json()
                for item in items:
                    if item['type'] == 'file' and item['name'].endswith('.md'):
                        try:
                            file_response = requests.get(item['download_url'], timeout=10)
                            if file_response.status_code == 200:
                                # Preserve directory structure
                                relative_path = item['path'].replace(f"{path}/", "").replace(path, "")
                                if relative_path:
                                    file_path = target_dir / relative_path
                                    file_path.parent.mkdir(parents=True, exist_ok=True)
                                else:
                                    file_path = target_dir / item['name']
                                file_path.write_text(file_response.text, encoding='utf-8')
                                print(f"    [OK] {item['path']} downloaded")
                        except Exception as e:
                            print(f"    [WARN] Failed to download {item['name']}: {e}")
                    elif item['type'] == 'dir' and current_depth < max_depth - 1:
                        # Recursively download subdirectories
                        subdir = target_dir / item['name']
                        subdir.mkdir(parents=True, exist_ok=True)
                        self._download_github_docs_recursive(owner, repo, item['path'], subdir, max_depth, current_depth + 1)
        except Exception as e:
            print(f"    [WARN] Failed to list {path}: {e}")
    
    def _is_doc_page(self, url: str, base_url: str) -> bool:
        """Check if URL is a documentation page."""
        parsed_base = urlparse(base_url)
        parsed_url = urlparse(url)
        
        # Same domain
        if parsed_url.netloc != parsed_base.netloc:
            return False
        
        # Not external links
        if not url.startswith(base_url):
            return False
        
        # Common doc patterns
        doc_patterns = ['/docs/', '/documentation/', '/guide/', '/tutorial/', '/api/']
        return any(pattern in url.lower() for pattern in doc_patterns) or url == base_url
    
    def _url_to_filename(self, url: str) -> str:
        """Convert URL to safe filename."""
        parsed = urlparse(url)
        path = parsed.path.strip('/').replace('/', '_')
        if not path:
            path = "index"
        if not path.endswith('.md'):
            path += '.md'
        return path
    
    def ingest_to_rag(self):
        """Ingest downloaded docs into RAG."""
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from src.agentic.tools.local_rag import get_local_rag
            
            rag = get_local_rag()
            if not rag:
                print("  [SKIP] RAG not available (get_local_rag returned None)")
                return
            
            if not hasattr(rag, 'is_available') or not rag.is_available():
                print("  [SKIP] RAG not available (is_available() returned False)")
                return
            
            # Ingest all markdown files (recursive)
            md_files = list(self.docs_dir.rglob("*.md"))
            for md_file in md_files:
                try:
                    content = md_file.read_text(encoding='utf-8')
                    # Generate doc_id from relative path
                    try:
                        rel_path = md_file.relative_to(self.docs_dir)
                        doc_id = f"framework:{self.framework_name}:{str(rel_path).replace('\\', '/')}"
                    except:
                        doc_id = f"framework:{self.framework_name}:{md_file.name}"
                    
                    # Add to RAG with framework name as metadata
                    rag.add_document(
                        doc_id=doc_id,
                        content=content,
                        metadata={
                            "source": f"framework:{self.framework_name}",
                            "file": md_file.name,
                            "type": "framework_docs",
                            "framework": self.framework_name
                        }
                    )
                    print(f"    [OK] Ingested {md_file.name}")
                except Exception as e:
                    print(f"    [WARN] Failed to ingest {md_file.name}: {e}")
                    
        except ImportError:
            print("  [SKIP] RAG not available (import failed)")
        except Exception as e:
            print(f"  [WARN] RAG ingestion failed: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/install_framework.py <framework_name>")
        print("\nExamples:")
        print("  python scripts/install_framework.py crewai")
        print("  python scripts/install_framework.py autogen")
        print("  python scripts/install_framework.py swarm")
        sys.exit(1)
    
    framework_name = sys.argv[1]
    installer = FrameworkInstaller(framework_name)
    installer.install()


if __name__ == "__main__":
    main()


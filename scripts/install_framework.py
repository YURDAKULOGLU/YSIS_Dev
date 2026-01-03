#!/usr/bin/env python3
"""
Framework Installer with Automatic Documentation Download
Installs framework and automatically downloads all documentation to RAG.
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
    "langgraph": "https://langchain-ai.github.io/langgraph/",
    "litellm": "https://docs.litellm.ai/",
    "redis": "https://redis.io/docs/",
    "crewai": "https://docs.crewai.com/",
    "autogen": "https://microsoft.github.io/autogen/",
    "ollama": "https://ollama.ai/docs/",
    "instructor": "https://github.com/jxnl/instructor",  # GitHub-based
    "swarm": None,  # Check GitHub
    "autogpt": None,  # Check GitHub
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
            
            # Download each page
            for i, url in enumerate(set(links)[:50], 1):  # Limit to 50 pages
                try:
                    print(f"  [{i}/{min(50, len(set(links)))}] Downloading {url}...")
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
            self._download_github_docs(f"https://github.com/{self.framework_name}")
    
    def _download_github_docs(self, repo_url: str):
        """Download documentation from GitHub repo."""
        print(f"  Downloading from GitHub: {repo_url}...")
        
        # Try to get README
        try:
            if "github.com" in repo_url:
                # Extract owner/repo
                parts = repo_url.replace("https://github.com/", "").split("/")
                if len(parts) >= 2:
                    owner, repo = parts[0], parts[1]
                    
                    # Download README
                    readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
                    try:
                        readme_response = requests.get(readme_url, timeout=10)
                        if readme_response.status_code == 200:
                            (self.docs_dir / "README.md").write_text(readme_response.text, encoding='utf-8')
                            print(f"    [OK] README.md downloaded")
                    except:
                        pass
                    
                    # Try docs/ folder
                    docs_url = f"https://api.github.com/repos/{owner}/{repo}/contents/docs"
                    try:
                        docs_response = requests.get(docs_url, timeout=10)
                        if docs_response.status_code == 200:
                            docs_files = docs_response.json()
                            for file_info in docs_files:
                                if file_info['type'] == 'file' and file_info['name'].endswith('.md'):
                                    file_url = file_info['download_url']
                                    file_response = requests.get(file_url, timeout=10)
                                    (self.docs_dir / file_info['name']).write_text(file_response.text, encoding='utf-8')
                                    print(f"    [OK] {file_info['name']} downloaded")
                    except:
                        pass
        except Exception as e:
            print(f"    [WARN] GitHub download failed: {e}")
    
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
            from src.agentic.tools.local_rag import get_local_rag
            
            rag = get_local_rag()
            if not rag or not rag.is_available():
                print("  [SKIP] RAG not available")
                return
            
            # Ingest all markdown files
            md_files = list(self.docs_dir.glob("*.md"))
            for md_file in md_files:
                try:
                    content = md_file.read_text(encoding='utf-8')
                    # Add to RAG with framework name as metadata
                    rag.add_document(
                        content=content,
                        metadata={
                            "source": f"framework:{self.framework_name}",
                            "file": md_file.name,
                            "type": "framework_docs"
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


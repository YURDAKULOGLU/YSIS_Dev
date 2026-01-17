#!/usr/bin/env python3
"""
🚀 ENHANCED Automatic Package Documentation Scraper
Scrapes documentation for ALL packages in requirements.txt automatically.

Features:
- ✅ Parses requirements.txt
- ✅ Gets package metadata from PyPI (with retry)
- ✅ Finds documentation URLs (PyPI, GitHub, docs sites)
- ✅ Scrapes documentation automatically
- ✅ Saves to platform_data/knowledge/Frameworks/{package_name}/
- ✅ Supports multiple sources: PyPI, GitHub, official docs sites
- ✅ Retry mechanism with exponential backoff
- ✅ Progress tracking
- ✅ Rate limiting
- ✅ Session management
- ✅ Better error handling
- ✅ Statistics tracking
"""

import re
import sys
import json
import time
import random
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, field
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import markdownify

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(PROJECT_ROOT / "logs" / "scraper.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class PackageInfo:
    """Package information from PyPI."""
    name: str
    version: Optional[str] = None
    description: Optional[str] = None
    home_page: Optional[str] = None
    project_urls: Dict[str, str] = None
    documentation_url: Optional[str] = None
    github_url: Optional[str] = None
    docs_site_url: Optional[str] = None
    scraped_at: Optional[str] = None

@dataclass
class ScrapingStats:
    """Statistics for scraping session."""
    total_packages: int = 0
    processed: int = 0
    success: int = 0
    failed: int = 0
    skipped: int = 0
    start_time: float = field(default_factory=time.time)
    errors: List[str] = field(default_factory=list)
    
    @property
    def elapsed_time(self) -> float:
        return time.time() - self.start_time
    
    @property
    def success_rate(self) -> float:
        if self.processed == 0:
            return 0.0
        return (self.success / self.processed) * 100

class PackageDocScraper:
    """🚀 Enhanced scraper for Python packages documentation."""
    
    def __init__(self, requirements_file: str = "requirements.txt", max_workers: int = 3):
        self.requirements_file = Path(requirements_file)
        self.packages: List[str] = []
        self.package_info: Dict[str, PackageInfo] = {}
        self.docs_base = PROJECT_ROOT / "platform_data" / "knowledge" / "Frameworks"
        self.docs_base.mkdir(parents=True, exist_ok=True)
        self.stats = ScrapingStats()
        self.max_workers = max_workers  # For future parallel processing
        
        # Create session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set user agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Framework-specific documentation URLs
        self.framework_docs = {
            "aider": "https://aider.chat/docs/",
            "langgraph": "https://langchain-ai.github.io/langgraph/",
            "litellm": "https://docs.litellm.ai/",
            "redis": "https://redis.io/docs/",
            "crewai": "https://docs.crewai.com/",
            "autogen": "https://microsoft.github.io/autogen/",
            "pyautogen": "https://microsoft.github.io/autogen/",
            "ollama": "https://ollama.ai/docs/",
            "instructor": "https://github.com/jxnl/instructor",
            "temporalio": "https://docs.temporal.io/",
            "ray": "https://docs.ray.io/",
            "prefect": "https://docs.prefect.io/",
            "spade": "https://spadeagents.eu/docs/",
            "celery": "https://docs.celeryproject.org/",
            "llama-index": "https://docs.llamaindex.ai/",
            "llama-index-core": "https://docs.llamaindex.ai/",
            "langchain": "https://python.langchain.com/",
            "pydantic": "https://docs.pydantic.dev/",
            "fastapi": "https://fastapi.tiangolo.com/",
            "streamlit": "https://docs.streamlit.io/",
        }
        
        # Framework-specific GitHub repo mappings
        self.repo_mappings = {
            "prefect": ("prefecthq", "prefect"),
            "spade": ("javipalanca", "spade"),
            "celery": ("celery", "celery"),
            "temporalio": ("temporalio", "python-sdk"),
            "ray": ("ray-project", "ray"),
            "pyautogen": ("microsoft", "autogen"),
            "autogen": ("microsoft", "autogen"),
            "swarm": ("swarm-ai", "swarm"),
            "autogpt": ("Significant-Gravitas", "AutoGPT"),
            "langgraph": ("langchain-ai", "langgraph"),
            "litellm": ("BerriAI", "litellm"),
            "instructor": ("jxnl", "instructor"),
            "ollama": ("ollama", "ollama"),
            "llama-index": ("run-llama", "llama_index"),
            "llama-index-core": ("run-llama", "llama_index"),
            "langchain": ("langchain-ai", "langchain"),
            "pydantic": ("pydantic", "pydantic"),
            "fastapi": ("tiangolo", "fastapi"),
            "streamlit": ("streamlit", "streamlit"),
        }
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.3  # Reduced from 0.5s to 0.3s for faster scraping
        
    def _rate_limit(self):
        """Rate limiting to be nice to servers."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def parse_requirements(self) -> List[str]:
        """Parse requirements.txt and extract package names."""
        if not self.requirements_file.exists():
            logger.error(f"{self.requirements_file} not found!")
            return []
        
        packages = []
        with open(self.requirements_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Parse package name (handle version specifiers)
                match = re.match(r'^([a-zA-Z0-9_-]+(?:\[[^\]]+\])?)', line)
                if match:
                    package_name = match.group(1)
                    # Remove extras: package[extra] -> package
                    package_name = re.sub(r'\[.*\]', '', package_name)
                    packages.append(package_name)
        
        self.packages = packages
        self.stats.total_packages = len(packages)
        logger.info(f"Found {len(packages)} packages in requirements.txt")
        return packages
    
    def get_pypi_metadata(self, package_name: str, retries: int = 3) -> Optional[PackageInfo]:
        """Get package metadata from PyPI with retry."""
        for attempt in range(retries):
            try:
                self._rate_limit()
                url = f"https://pypi.org/pypi/{package_name}/json"
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                data = response.json()
                info = data.get('info', {})
                
                # Extract URLs
                home_page = info.get('home_page') or info.get('project_url')
                project_urls = info.get('project_urls', {}) or {}
                
                # Find documentation URL
                docs_url = None
                github_url = None
                
                # Check project_urls for documentation
                for key, url in project_urls.items():
                    key_lower = key.lower()
                    if 'doc' in key_lower or 'documentation' in key_lower:
                        docs_url = url
                    elif 'github' in key_lower or 'source' in key_lower or 'code' in key_lower:
                        github_url = url
                
                # If no docs URL, try to infer from home_page
                if not docs_url and home_page:
                    if any(pattern in home_page.lower() for pattern in ['docs', 'documentation', 'readthedocs']):
                        docs_url = home_page
                    elif 'github.com' in home_page:
                        github_url = home_page
                
                return PackageInfo(
                    name=package_name,
                    version=info.get('version'),
                    description=info.get('summary'),
                    home_page=home_page,
                    project_urls=project_urls,
                    documentation_url=docs_url,
                    github_url=github_url,
                    scraped_at=datetime.now().isoformat()
                )
            except requests.exceptions.RequestException as e:
                if attempt < retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Attempt {attempt + 1} failed for {package_name}, retrying in {wait_time:.2f}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Could not fetch PyPI metadata for {package_name} after {retries} attempts: {e}")
                    self.stats.errors.append(f"{package_name}: PyPI metadata fetch failed")
            except Exception as e:
                logger.error(f"Error fetching metadata for {package_name}: {e}")
                self.stats.errors.append(f"{package_name}: {str(e)}")
                return None
        
        return None
    
    def find_documentation_url(self, package_info: PackageInfo) -> Optional[str]:
        """Find the best documentation URL for a package."""
        package_name = package_info.name.lower()
        
        # Priority 1: Framework-specific mapping
        if package_name in self.framework_docs:
            docs_url = self.framework_docs[package_name]
            if docs_url:
                return docs_url
        
        # Priority 2: Explicit documentation_url from PyPI
        if package_info.documentation_url:
            return package_info.documentation_url
        
        # Priority 3: GitHub README/docs folder
        if package_info.github_url:
            github_docs = f"{package_info.github_url.rstrip('/')}/tree/main/docs"
            if self._url_exists(github_docs):
                return github_docs
        
        # Priority 4: Inferred from home_page
        if package_info.home_page:
            parsed = urlparse(package_info.home_page)
            if parsed.netloc:
                domain = parsed.netloc
                # Try docs.{domain}
                docs_url = f"{parsed.scheme}://docs.{domain}"
                if self._url_exists(docs_url):
                    return docs_url
                
                # Try {domain}/docs
                docs_url = f"{parsed.scheme}://{domain}/docs"
                if self._url_exists(docs_url):
                    return docs_url
        
        return None
    
    def _url_exists(self, url: str, quick: bool = True) -> bool:
        """Check if URL exists (quick HEAD request with retry)."""
        try:
            self._rate_limit()
            # Use HEAD for quick check, but GET with stream=True for more reliable check
            if quick:
                response = self.session.head(url, timeout=3, allow_redirects=True)
            else:
                response = self.session.get(url, timeout=3, allow_redirects=True, stream=True)
                response.close()  # Close connection immediately
            # Accept both 200 and 301/302 (redirects are OK)
            return response.status_code in (200, 301, 302, 303, 307, 308)
        except requests.exceptions.RequestException:
            return False
        except Exception:
            return False
    
    def scrape_documentation(self, package_name: str, docs_url: str) -> bool:
        """Scrape documentation from URL."""
        package_dir = self.docs_base / package_name
        package_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Scraping {package_name} from {docs_url}...")
        
        # Determine scraping method based on URL
        if 'github.com' in docs_url:
            return self._scrape_github_docs(package_name, docs_url, package_dir)
        elif any(pattern in docs_url for pattern in ['readthedocs', 'docs.', 'documentation', 'github.io']):
            return self._scrape_docs_site(package_name, docs_url, package_dir)
        else:
            return self._scrape_generic(package_name, docs_url, package_dir)
    
    def _scrape_github_docs(self, package_name: str, github_url: str, output_dir: Path) -> bool:
        """Scrape documentation from GitHub."""
        try:
            # Check repo mappings first
            package_name_lower = package_name.lower()
            if package_name_lower in self.repo_mappings:
                owner, repo = self.repo_mappings[package_name_lower]
                github_url = f"https://github.com/{owner}/{repo}"
            else:
                match = re.match(r'https://github\.com/([^/]+)/([^/]+)', github_url)
                if not match:
                    return False
                owner, repo = match.groups()
            
            # Try to get README (try multiple branches)
            readme_downloaded = False
            for branch in ["main", "master", "develop"]:
                readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
                try:
                    self._rate_limit()
                    readme_response = self.session.get(readme_url, timeout=10)
                    if readme_response.status_code == 200:
                        readme_path = output_dir / "README.md"
                        readme_path.write_text(readme_response.text, encoding='utf-8')
                        logger.info(f"Downloaded README.md from {branch} branch")
                        readme_downloaded = True
                        break
                except Exception as e:
                    logger.debug(f"Failed to get README from {branch}: {e}")
                    continue
            
            # Try docs/ folder (recursive)
            docs_dir = output_dir / "docs"
            docs_dir.mkdir(exist_ok=True)
            self._download_github_docs_recursive(owner, repo, "docs", docs_dir)
            
            return readme_downloaded or (docs_dir.exists() and any(docs_dir.iterdir()))
        except Exception as e:
            logger.error(f"Failed to scrape GitHub docs for {package_name}: {e}")
            self.stats.errors.append(f"{package_name}: GitHub scrape failed - {str(e)}")
            return False
    
    def _download_github_docs_recursive(self, owner: str, repo: str, path: str, target_dir: Path, max_depth: int = 3, current_depth: int = 0):
        """Recursively download docs from GitHub."""
        if current_depth >= max_depth:
            return
        
        try:
            self._rate_limit()
            docs_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
            docs_response = self.session.get(docs_url, timeout=10)
            if docs_response.status_code == 200:
                items = docs_response.json()
                for item in items:
                    if item['type'] == 'file' and item['name'].endswith('.md'):
                        try:
                            self._rate_limit()
                            file_response = self.session.get(item['download_url'], timeout=10)
                            if file_response.status_code == 200:
                                relative_path = item['path'].replace(f"{path}/", "").replace(path, "")
                                if relative_path:
                                    file_path = target_dir / relative_path
                                    file_path.parent.mkdir(parents=True, exist_ok=True)
                                else:
                                    file_path = target_dir / item['name']
                                file_path.write_text(file_response.text, encoding='utf-8')
                                logger.debug(f"Downloaded {item['path']}")
                        except Exception as e:
                            logger.warning(f"Failed to download {item['name']}: {e}")
                    elif item['type'] == 'dir' and current_depth < max_depth - 1:
                        subdir = target_dir / item['name']
                        subdir.mkdir(parents=True, exist_ok=True)
                        self._download_github_docs_recursive(owner, repo, item['path'], subdir, max_depth, current_depth + 1)
        except Exception as e:
            logger.warning(f"Failed to list {path}: {e}")
    
    def _scrape_docs_site(self, package_name: str, base_url: str, output_dir: Path) -> bool:
        """Scrape documentation site (ReadTheDocs, etc.) with improved link handling."""
        try:
            # Follow redirects and get actual base URL
            self._rate_limit()
            initial_response = self.session.get(base_url, timeout=15, allow_redirects=True)
            actual_base_url = initial_response.url
            logger.debug(f"Base URL redirected: {base_url} -> {actual_base_url}")
            
            # Extract version prefix if exists (e.g., /en/stable/, /latest/)
            parsed_base = urlparse(actual_base_url)
            version_prefix = None
            path_parts = parsed_base.path.strip('/').split('/')
            
            # Common version patterns: /en/stable/, /latest/, /v1.0/, etc.
            if len(path_parts) >= 2:
                # Check for language/version pattern (en/stable, latest, etc.)
                if path_parts[0] in ['en', 'tr', 'fr', 'de', 'es', 'ja', 'zh'] and path_parts[1] in ['stable', 'latest', 'dev']:
                    version_prefix = f"/{path_parts[0]}/{path_parts[1]}"
                elif path_parts[0] in ['latest', 'stable', 'dev', 'main']:
                    version_prefix = f"/{path_parts[0]}"
                elif path_parts[0].startswith('v') and path_parts[0][1:].replace('.', '').isdigit():
                    version_prefix = f"/{path_parts[0]}"
            
            # Normalize base URL (remove trailing slash)
            actual_base_url = actual_base_url.rstrip('/')
            base_domain = urlparse(actual_base_url).netloc
            
            logger.debug(f"Detected version prefix: {version_prefix}")
            
            visited = set()
            to_visit = [actual_base_url]
            docs_dir = output_dir / "docs"
            docs_dir.mkdir(exist_ok=True)
            
            max_pages = getattr(self, 'max_pages', 100)  # Allow override via argument
            pages_scraped = 0
            failed_urls = []
            
            while to_visit and pages_scraped < max_pages:
                url = to_visit.pop(0)
                
                if url in visited:
                    continue
                
                visited.add(url)
                
                try:
                    self._rate_limit()
                    response = self.session.get(url, timeout=15, allow_redirects=True)
                    
                    # Check if URL is valid (not 404 or other errors)
                    if response.status_code == 404:
                        failed_urls.append(url)
                        logger.debug(f"Skipping 404: {url}")
                        continue
                    
                    # Skip other client/server errors
                    if response.status_code >= 400:
                        failed_urls.append(url)
                        logger.debug(f"Skipping {response.status_code}: {url}")
                        continue
                    
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style", "nav", "footer", "header"]):
                        script.decompose()
                    
                    # Convert to markdown
                    markdown_content = markdownify.markdownify(str(soup), heading_style="ATX")
                    
                    # Save page
                    page_name = urlparse(response.url).path.strip('/').replace('/', '_') or 'index'
                    if not page_name.endswith('.md'):
                        page_name += '.md'
                    # Sanitize filename
                    page_name = re.sub(r'[<>:"|?*]', '_', page_name)
                    
                    page_path = docs_dir / page_name
                    page_path.write_text(markdown_content, encoding='utf-8')
                    pages_scraped += 1
                    
                    if pages_scraped % 10 == 0:
                        logger.info(f"  Scraped {pages_scraped} pages...")
                    
                    # Find links to other pages (improved logic)
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        
                        # Skip anchors, mailto, javascript, etc.
                        if href.startswith(('#', 'mailto:', 'javascript:', 'tel:')):
                            continue
                        
                        # Resolve relative URLs using current page URL (not base_url)
                        # This is critical for relative links like ../concepts/
                        current_page_url = response.url
                        full_url = urljoin(current_page_url, href)
                        parsed = urlparse(full_url)
                        
                        # Only follow links from same domain
                        if parsed.netloc != base_domain:
                            continue
                        
                        # Remove fragment (#anchor)
                        full_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                        if parsed.query:
                            full_url += f"?{parsed.query}"
                        
                        # Fix common issues:
                        # 1. Remove .md extension (docs sites usually don't use it in URLs)
                        if full_url.endswith('.md'):
                            full_url = full_url[:-3]
                        
                        # 2. Remove .html extension (some sites use it, some don't)
                        if full_url.endswith('.html'):
                            full_url = full_url[:-5]
                        
                        # 3. Normalize URL (remove trailing slash for consistency, we'll add it back in variations)
                        full_url = full_url.rstrip('/')
                        
                        # Skip if already visited or invalid
                        if (full_url in visited or
                            '#' in full_url.split('/')[-1] or
                            any(ext in full_url.lower() for ext in ['.pdf', '.zip', '.tar.gz', '.jpg', '.png', '.gif', '.svg', '.ico', '.css', '.js', '.json', '.xml', '.woff', '.woff2', '.ttf', '.eot'])):
                            continue
                        
                        # Skip common non-documentation paths
                        skip_paths = ['/search', '/api/', '/_static/', '/_images/', '/assets/', '/static/', '/media/']
                        if any(skip_path in full_url.lower() for skip_path in skip_paths):
                            continue
                        
                        # Build URL variations with smart version prefix handling
                        url_variations = []
                        
                        # If version prefix exists and URL doesn't have it, try adding it
                        if version_prefix and version_prefix not in full_url:
                            # Extract path from URL
                            url_path = parsed.path
                            
                            # If path doesn't start with version prefix, add it
                            if not url_path.startswith(version_prefix):
                                # Remove leading slash if exists
                                url_path = url_path.lstrip('/')
                                # Add version prefix
                                url_with_version = f"{parsed.scheme}://{parsed.netloc}{version_prefix}/{url_path}"
                                url_variations.append(url_with_version)
                                url_variations.append(f"{url_with_version}/")  # With trailing slash
                        
                        # Add original URL variations
                        url_variations.append(full_url)
                        if not full_url.endswith('/'):
                            url_variations.append(f"{full_url}/")
                        
                        # Try .html extension
                        if not full_url.endswith('.html'):
                            url_variations.append(f"{full_url}.html")
                            url_variations.append(f"{full_url}.html/")
                        
                        # Validate URL before adding (optimized: try 2 variations first, then 3 more if needed)
                        valid_url = None
                        # Try first 2 variations (most common cases) - faster
                        for url_var in url_variations[:2]:
                            if self._url_exists(url_var, quick=True):
                                valid_url = url_var
                                break
                        # If first 2 failed, try remaining variations
                        if not valid_url and len(url_variations) > 2:
                            for url_var in url_variations[2:5]:
                                if self._url_exists(url_var, quick=True):
                                    valid_url = url_var
                                    break
                        
                        if valid_url:
                            if valid_url not in visited:
                                to_visit.append(valid_url)
                        else:
                            # Log only if it looks like a doc URL (not external links)
                            doc_patterns = ['/docs/', '/documentation/', '/guide/', '/tutorial/', '/api/', '/reference/', 
                                          '/concepts/', '/howtos/', '/getstarted/', '/tutorials/']
                            if any(pattern in full_url.lower() for pattern in doc_patterns):
                                logger.debug(f"Skipping invalid URL: {full_url} (tried {len(url_variations)} variations)")
                    
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 404:
                        failed_urls.append(url)
                        logger.debug(f"404 for {url}")
                    else:
                        logger.warning(f"HTTP error for {url}: {e}")
                    continue
                except Exception as e:
                    logger.warning(f"Failed to scrape {url}: {e}")
                    continue
            
            if failed_urls:
                logger.info(f"Skipped {len(failed_urls)} invalid URLs (404s)")
            
            logger.info(f"Scraped {pages_scraped} pages from {actual_base_url}")
            return pages_scraped > 0
        except Exception as e:
            logger.error(f"Failed to scrape docs site for {package_name}: {e}")
            self.stats.errors.append(f"{package_name}: Docs site scrape failed - {str(e)}")
            return False
    
    def _scrape_generic(self, package_name: str, url: str, output_dir: Path) -> bool:
        """Generic scraping for unknown URL types."""
        try:
            self._rate_limit()
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            markdown_content = markdownify.markdownify(str(soup), heading_style="ATX")
            
            page_path = output_dir / "index.md"
            page_path.write_text(markdown_content, encoding='utf-8')
            logger.info(f"Scraped generic page for {package_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to scrape generic page for {package_name}: {e}")
            self.stats.errors.append(f"{package_name}: Generic scrape failed - {str(e)}")
            return False
    
    def save_package_metadata(self, package_name: str, package_info: PackageInfo):
        """Save package metadata to JSON."""
        metadata_dir = self.docs_base / package_name
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            "name": package_info.name,
            "version": package_info.version,
            "description": package_info.description,
            "home_page": package_info.home_page,
            "documentation_url": package_info.documentation_url,
            "github_url": package_info.github_url,
            "project_urls": package_info.project_urls or {},
            "scraped_at": package_info.scraped_at or datetime.now().isoformat(),
        }
        
        metadata_path = metadata_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def process_all_packages(self, skip_existing: bool = True):
        """Process all packages in requirements.txt."""
        packages = self.parse_requirements()
        
        if not packages:
            logger.error("No packages found!")
            return
        
        logger.info(f"Processing {len(packages)} packages...\n")
        
        results = {
            "success": [],
            "failed": [],
            "skipped": [],
        }
        
        for i, package_name in enumerate(packages, 1):
            logger.info(f"\n[{i}/{len(packages)}] Processing {package_name}...")
            self.stats.processed += 1
            
            # Check if already scraped (faster check - just metadata.json and docs/*.md)
            package_dir = self.docs_base / package_name
            if skip_existing:
                metadata_file = package_dir / "metadata.json"
                docs_dir = package_dir / "docs"
                # Quick check: metadata.json exists and docs/*.md exists
                if metadata_file.exists() and (docs_dir.exists() and any(docs_dir.glob("*.md"))):
                    logger.debug(f"  [SKIP] Documentation already exists for {package_name}")
                    results["skipped"].append(package_name)
                    self.stats.skipped += 1
                    continue
            
            # Get PyPI metadata
            package_info = self.get_pypi_metadata(package_name)
            if not package_info:
                logger.warning(f"Could not get metadata for {package_name}")
                results["failed"].append(package_name)
                self.stats.failed += 1
                continue
            
            self.package_info[package_name] = package_info
            self.save_package_metadata(package_name, package_info)
            
            # Find documentation URL
            docs_url = self.find_documentation_url(package_info)
            if not docs_url:
                logger.warning(f"No documentation URL found for {package_name}")
                logger.debug(f"  Home: {package_info.home_page}")
                logger.debug(f"  GitHub: {package_info.github_url}")
                results["failed"].append(package_name)
                self.stats.failed += 1
                continue
            
            # Scrape documentation
            try:
                if self.scrape_documentation(package_name, docs_url):
                    results["success"].append(package_name)
                    self.stats.success += 1
                else:
                    results["failed"].append(package_name)
                    self.stats.failed += 1
            except KeyboardInterrupt:
                logger.warning("Scraping interrupted by user")
                raise
            except Exception as e:
                logger.error(f"Unexpected error scraping {package_name}: {e}")
                results["failed"].append(package_name)
                self.stats.failed += 1
                self.stats.errors.append(f"{package_name}: Unexpected error - {str(e)}")
        
        # Print summary
        self._print_summary(results)
        
        # Save results
        self._save_results(results)
    
    def _print_summary(self, results: Dict):
        """Print scraping summary."""
        print("\n" + "="*70)
        print("📊 SCRAPING SUMMARY")
        print("="*70)
        print(f"✅ Success: {len(results['success'])} ({self.stats.success_rate:.1f}%)")
        print(f"❌ Failed: {len(results['failed'])}")
        print(f"⏭️  Skipped: {len(results['skipped'])}")
        print(f"⏱️  Elapsed: {self.stats.elapsed_time:.1f}s")
        print(f"📦 Total: {self.stats.total_packages}")
        
        if results['success']:
            print(f"\n✅ Successfully scraped ({len(results['success'])}):")
            for pkg in results['success'][:10]:  # Show first 10
                print(f"  • {pkg}")
            if len(results['success']) > 10:
                print(f"  ... and {len(results['success']) - 10} more")
        
        if results['failed']:
            print(f"\n❌ Failed to scrape ({len(results['failed'])}):")
            for pkg in results['failed'][:10]:  # Show first 10
                print(f"  • {pkg}")
            if len(results['failed']) > 10:
                print(f"  ... and {len(results['failed']) - 10} more")
        
        if self.stats.errors:
            print(f"\n⚠️  Errors ({len(self.stats.errors)}):")
            for error in self.stats.errors[:5]:  # Show first 5
                print(f"  • {error}")
            if len(self.stats.errors) > 5:
                print(f"  ... and {len(self.stats.errors) - 5} more")
    
    def _save_results(self, results: Dict):
        """Save scraping results."""
        results_data = {
            "timestamp": datetime.now().isoformat(),
            "stats": {
                "total": self.stats.total_packages,
                "success": self.stats.success,
                "failed": self.stats.failed,
                "skipped": self.stats.skipped,
                "elapsed_time": self.stats.elapsed_time,
                "success_rate": self.stats.success_rate,
            },
            "results": results,
            "errors": self.stats.errors,
        }
        
        results_path = self.docs_base / "scraping_results.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {results_path}")
        
        if results['success']:
            print(f"\n💡 To ingest docs into RAG, run:")
            print(f"   python scripts/ingest_docs_to_rag.py --frameworks")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🚀 Enhanced automatic documentation scraper for requirements.txt packages"
    )
    parser.add_argument(
        "--requirements",
        default="requirements.txt",
        help="Path to requirements.txt file"
    )
    parser.add_argument(
        "--no-skip",
        action="store_true",
        help="Re-scrape even if documentation already exists"
    )
    parser.add_argument(
        "--package",
        help="Scrape only a specific package (instead of all)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=100,
        help="Maximum pages to scrape per package (default: 100)"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    scraper = PackageDocScraper(args.requirements)
    scraper.max_pages = args.max_pages  # Set max pages from argument
    
    if args.package:
        # Scrape single package
        logger.info(f"Scraping single package: {args.package}")
        package_info = scraper.get_pypi_metadata(args.package)
        if package_info:
            scraper.save_package_metadata(args.package, package_info)
            docs_url = scraper.find_documentation_url(package_info)
            if docs_url:
                scraper.scrape_documentation(args.package, docs_url)
            else:
                logger.error(f"No documentation URL found for {args.package}")
        else:
            logger.error(f"Could not get metadata for {args.package}")
    else:
        # Scrape all packages
        scraper.process_all_packages(skip_existing=not args.no_skip)

if __name__ == "__main__":
    main()


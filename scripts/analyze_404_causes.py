#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze 404 causes in documentation scraping.
"""

import sys
import io
# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def analyze_404_causes(base_url: str):
    """Analyze why some links return 404."""
    print(f"\nAnalyzing 404 causes for: {base_url}\n")
    print("="*70)
    
    # Get the page
    response = requests.get(base_url, allow_redirects=True)
    actual_url = response.url
    print(f"Base URL: {base_url}")
    print(f"Actual URL (after redirect): {actual_url}\n")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all links
    all_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith(('#', 'mailto:', 'javascript:', 'tel:')):
            continue
        
        # Resolve relative URLs
        full_url = urljoin(actual_url, href)
        all_links.append((href, full_url))
    
    print(f"Found {len(all_links)} links\n")
    
    # Test each link
    issues = {
        'missing_version_prefix': [],
        'wrong_extension': [],
        'trailing_slash': [],
        'broken_links': [],
        'external_links': [],
        'working': []
    }
    
    for original_href, full_url in all_links[:30]:  # Test first 30
        parsed = urlparse(full_url)
        
        # Skip external links
        if parsed.netloc != urlparse(actual_url).netloc:
            issues['external_links'].append((original_href, full_url))
            continue
        
        # Test original URL
        test_response = requests.head(full_url, allow_redirects=True, timeout=5)
        
        if test_response.status_code == 200:
            issues['working'].append(full_url)
        elif test_response.status_code == 404:
            # Analyze why it's 404
            
            # Check 1: Missing version prefix
            if '/en/stable/' in actual_url and '/en/stable/' not in full_url:
                # Try with version prefix
                version_url = urljoin(actual_url, full_url.replace(urlparse(actual_url).netloc, ''))
                if '/en/stable/' not in version_url:
                    path = parsed.path
                    if not path.startswith('/en/stable/'):
                        version_url = f"{parsed.scheme}://{parsed.netloc}/en/stable{path}"
                        version_test = requests.head(version_url, allow_redirects=True, timeout=5)
                        if version_test.status_code == 200:
                            issues['missing_version_prefix'].append((full_url, version_url))
                            continue
            
            # Check 2: Wrong extension (.md)
            if full_url.endswith('.md'):
                no_ext_url = full_url[:-3]
                no_ext_test = requests.head(no_ext_url, allow_redirects=True, timeout=5)
                if no_ext_test.status_code == 200:
                    issues['wrong_extension'].append((full_url, no_ext_url))
                    continue
            
            # Check 3: Trailing slash
            if not full_url.endswith('/'):
                with_slash = f"{full_url}/"
                slash_test = requests.head(with_slash, allow_redirects=True, timeout=5)
                if slash_test.status_code == 200:
                    issues['trailing_slash'].append((full_url, with_slash))
                    continue
                elif not full_url.endswith('.html'):
                    html_url = f"{full_url}.html"
                    html_test = requests.head(html_url, allow_redirects=True, timeout=5)
                    if html_test.status_code == 200:
                        issues['wrong_extension'].append((full_url, html_url))
                        continue
            
            # Check 4: Just broken
            issues['broken_links'].append(full_url)
    
    # Print results
    print("404 CAUSE ANALYSIS:\n")
    
    if issues['missing_version_prefix']:
        print(f"1. MISSING VERSION PREFIX ({len(issues['missing_version_prefix'])}):")
        print("   Links missing /en/stable/ prefix")
        for original, fixed in issues['missing_version_prefix'][:5]:
            print(f"   ❌ {original}")
            print(f"   ✅ {fixed}")
        print()
    
    if issues['wrong_extension']:
        print(f"2. WRONG EXTENSION ({len(issues['wrong_extension'])}):")
        print("   Links with .md or missing .html")
        for original, fixed in issues['wrong_extension'][:5]:
            print(f"   ❌ {original}")
            print(f"   ✅ {fixed}")
        print()
    
    if issues['trailing_slash']:
        print(f"3. TRAILING SLASH ({len(issues['trailing_slash'])}):")
        print("   Links missing trailing slash")
        for original, fixed in issues['trailing_slash'][:5]:
            print(f"   ❌ {original}")
            print(f"   ✅ {fixed}")
        print()
    
    if issues['broken_links']:
        print(f"4. BROKEN LINKS ({len(issues['broken_links'])}):")
        print("   Links that are actually broken (not fixable)")
        for url in issues['broken_links'][:5]:
            print(f"   [BROKEN] {url}")
        print()
    
    if issues['external_links']:
        print(f"5. EXTERNAL LINKS ({len(issues['external_links'])}):")
        print("   Links to other domains (skipped)")
        print()
    
    print(f"[OK] WORKING LINKS: {len(issues['working'])}")
    print()
    
    # Summary
    total_404s = (len(issues['missing_version_prefix']) + 
                  len(issues['wrong_extension']) + 
                  len(issues['trailing_slash']) + 
                  len(issues['broken_links']))
    
    print("="*70)
    print("SUMMARY:")
    print(f"  Total links tested: 30")
    print(f"  Working: {len(issues['working'])}")
    print(f"  404s (fixable): {total_404s - len(issues['broken_links'])}")
    print(f"  404s (broken): {len(issues['broken_links'])}")
    print(f"  External: {len(issues['external_links'])}")
    print()
    print("FIXABLE ISSUES:")
    print(f"  - Missing version prefix: {len(issues['missing_version_prefix'])}")
    print(f"  - Wrong extension: {len(issues['wrong_extension'])}")
    print(f"  - Trailing slash: {len(issues['trailing_slash'])}")
    print()
    print("UNFIXABLE ISSUES:")
    print(f"  - Actually broken links: {len(issues['broken_links'])}")
    print("="*70)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "https://docs.ragas.io"
    
    analyze_404_causes(base_url)


#!/usr/bin/env python3
"""
Limit Test for Package Documentation Scraper
Tests scraper with various edge cases and limits.
"""

import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.auto_scrape_package_docs import PackageDocScraper

def test_404_handling():
    """Test 404 error handling."""
    print("\n" + "="*70)
    print("TEST 1: 404 Error Handling")
    print("="*70)
    
    scraper = PackageDocScraper()
    
    # Test packages that might have 404s
    test_packages = [
        "ragas",  # Known to have some 404s
        "nonexistent-package-12345",  # Definitely doesn't exist
    ]
    
    for package in test_packages:
        print(f"\n[TEST] Testing {package}...")
        package_info = scraper.get_pypi_metadata(package)
        if package_info:
            docs_url = scraper.find_documentation_url(package_info)
            if docs_url:
                result = scraper.scrape_documentation(package, docs_url)
                print(f"  Result: {'SUCCESS' if result else 'FAILED'}")
            else:
                print(f"  Result: NO DOCS URL")
        else:
            print(f"  Result: NO METADATA (expected for nonexistent)")

def test_rate_limiting():
    """Test rate limiting."""
    print("\n" + "="*70)
    print("TEST 2: Rate Limiting")
    print("="*70)
    
    scraper = PackageDocScraper()
    
    # Test multiple rapid requests
    test_urls = [
        "https://pypi.org/pypi/requests/json",
        "https://pypi.org/pypi/beautifulsoup4/json",
        "https://pypi.org/pypi/pydantic/json",
    ]
    
    start_time = time.time()
    for i, url in enumerate(test_urls, 1):
        scraper._rate_limit()
        response = scraper.session.get(url, timeout=10)
        elapsed = time.time() - start_time
        print(f"  Request {i}: {response.status_code} (elapsed: {elapsed:.2f}s)")
    
    total_time = time.time() - start_time
    print(f"\n  Total time: {total_time:.2f}s")
    print(f"  Expected min: {len(test_urls) * scraper.min_request_interval:.2f}s")
    print(f"  Rate limiting: {'WORKING' if total_time >= len(test_urls) * scraper.min_request_interval else 'NOT WORKING'}")

def test_max_pages_limit():
    """Test max pages limit."""
    print("\n" + "="*70)
    print("TEST 3: Max Pages Limit")
    print("="*70)
    
    scraper = PackageDocScraper()
    
    # Test with a package that has many pages
    test_package = "llama-index"  # Known to have many pages
    
    package_info = scraper.get_pypi_metadata(test_package)
    if package_info:
        docs_url = scraper.find_documentation_url(package_info)
        if docs_url:
            print(f"  Testing with: {test_package}")
            print(f"  Docs URL: {docs_url}")
            print(f"  Max pages limit: 100")
            
            # Count existing pages
            package_dir = PROJECT_ROOT / "platform_data" / "knowledge" / "Frameworks" / test_package / "docs"
            if package_dir.exists():
                existing_pages = len(list(package_dir.glob("*.md")))
                print(f"  Existing pages: {existing_pages}")
                print(f"  Limit respected: {'YES' if existing_pages <= 100 else 'NO'}")

def test_retry_mechanism():
    """Test retry mechanism."""
    print("\n" + "="*70)
    print("TEST 4: Retry Mechanism")
    print("="*70)
    
    scraper = PackageDocScraper()
    
    # Test with a package that might fail
    test_package = "requests"  # Should work, but test retry logic
    
    print(f"  Testing retry with: {test_package}")
    package_info = scraper.get_pypi_metadata(test_package, retries=3)
    
    if package_info:
        print(f"  Metadata fetched successfully")
        print(f"    Name: {package_info.name}")
        print(f"    Version: {package_info.version}")
    else:
        print(f"  Failed to fetch metadata")

def test_concurrent_requests():
    """Test handling of concurrent-like requests."""
    print("\n" + "="*70)
    print("TEST 5: Concurrent Request Handling")
    print("="*70)
    
    scraper = PackageDocScraper()
    
    # Test multiple packages quickly
    test_packages = ["pydantic", "fastapi", "streamlit"]
    
    results = []
    start_time = time.time()
    
    for package in test_packages:
        package_info = scraper.get_pypi_metadata(package)
        if package_info:
            results.append((package, "OK"))
        else:
            results.append((package, "FAILED"))
    
    total_time = time.time() - start_time
    
    print(f"  Tested {len(test_packages)} packages")
    for package, status in results:
        print(f"    {package}: {status}")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Average per package: {total_time/len(test_packages):.2f}s")

def test_error_recovery():
    """Test error recovery."""
    print("\n" + "="*70)
    print("TEST 6: Error Recovery")
    print("="*70)
    
    scraper = PackageDocScraper()
    
    # Test with mix of valid and invalid
    test_cases = [
        ("pydantic", True),  # Should work
        ("nonexistent-package-xyz-123", False),  # Should fail gracefully
        ("fastapi", True),  # Should work
    ]
    
    for package, should_work in test_cases:
        print(f"\n  Testing: {package} (expected: {'OK' if should_work else 'FAIL'})")
        package_info = scraper.get_pypi_metadata(package)
        
        if package_info:
            print(f"    Metadata fetched")
        else:
            print(f"    {'Graceful failure' if not should_work else 'Unexpected failure'}")

def test_memory_usage():
    """Test memory usage with large scraping."""
    print("\n" + "="*70)
    print("TEST 7: Memory Usage")
    print("="*70)
    
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    scraper = PackageDocScraper()
    
    # Process a few packages
    test_packages = ["pydantic", "fastapi", "streamlit"]
    for package in test_packages:
        package_info = scraper.get_pypi_metadata(package)
    
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory
    
    print(f"  Initial memory: {initial_memory:.2f} MB")
    print(f"  Final memory: {final_memory:.2f} MB")
    print(f"  Increase: {memory_increase:.2f} MB")
    print(f"  Memory efficient: {'YES' if memory_increase < 50 else 'HIGH'}")

def main():
    """Run all limit tests."""
    import sys
    import io
    # Fix encoding for Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("\n" + "="*70)
    print("SCRAPER LIMIT TESTS")
    print("="*70)
    print("\nTesting scraper limits and error handling...")
    
    try:
        test_404_handling()
        test_rate_limiting()
        test_max_pages_limit()
        test_retry_mechanism()
        test_concurrent_requests()
        test_error_recovery()
        test_memory_usage()
        
        print("\n" + "="*70)
        print("ALL TESTS COMPLETED")
        print("="*70)
        print("\nNote: Some 404s and errors are expected and handled gracefully.")
        print("This is normal behavior for the scraper.")
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


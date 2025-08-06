#!/usr/bin/env python3
"""
Script to check for Liberation.fr RSS feeds by author
"""

import requests
import sys
from urllib.parse import urljoin

def check_rss_url(url):
    """Check if a URL returns a valid RSS feed"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content = response.text.lower()
            # Check for RSS indicators
            if any(indicator in content for indicator in ['<rss', '<feed', 'application/rss+xml', 'application/atom+xml']):
                return True, f"✓ RSS feed found at {url}"
            else:
                return False, f"✗ {url} returns content but doesn't appear to be RSS"
        else:
            return False, f"✗ {url} returned status {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"✗ Error accessing {url}: {str(e)}"

def main():
    base_url = "https://www.liberation.fr"
    author_slug = "benjamin-delille"
    
    # Common RSS URL patterns to test
    rss_patterns = [
        f"/auteur/{author_slug}/rss/",
        f"/auteur/{author_slug}/feed/",
        f"/auteur/{author_slug}.rss",
        f"/auteur/{author_slug}.xml",
        f"/rss/auteur/{author_slug}/",
        f"/feed/auteur/{author_slug}/",
        f"/auteur/{author_slug}/rss.xml",
        f"/auteur/{author_slug}/feed.xml"
    ]
    
    print(f"Checking RSS feed availability for author: {author_slug}")
    print("=" * 60)
    
    found_feeds = []
    
    for pattern in rss_patterns:
        url = urljoin(base_url, pattern)
        is_rss, message = check_rss_url(url)
        print(message)
        if is_rss:
            found_feeds.append(url)
    
    print("\n" + "=" * 60)
    if found_feeds:
        print(f"Found {len(found_feeds)} RSS feed(s):")
        for feed in found_feeds:
            print(f"  - {feed}")
    else:
        print("No RSS feeds found for this author.")
        print("\nAlternative suggestions:")
        print("1. Use the main Liberation.fr RSS feeds from:")
        print("   https://www.liberation.fr/liste-flux-rss/")
        print("2. Create a custom RSS feed using third-party services")
        print("3. Use web scraping tools to monitor the author's page")

if __name__ == "__main__":
    main()

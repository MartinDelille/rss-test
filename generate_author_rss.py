#!/usr/bin/env python3
"""
Custom RSS feed generator for Liberation.fr authors
This script scrapes an author's page and generates an RSS feed
"""

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
import re
from urllib.parse import urljoin, urlparse

def scrape_author_articles(author_url):
    """Scrape articles from an author's page"""
    try:
        response = requests.get(author_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        # Look for article links - this is based on the structure seen on the page
        # Liberation.fr seems to use specific patterns for article listings
        article_links = soup.find_all('a', href=re.compile(r'/\d{4}/'))
        
        for link in article_links[:10]:  # Limit to 10 most recent articles
            href = link.get('href')
            if href and href.startswith('/'):
                full_url = urljoin(author_url, href)
                title = link.get_text(strip=True)
                
                if title and len(title) > 10:  # Filter out short/empty titles
                    articles.append({
                        'title': title,
                        'url': full_url,
                        'description': title  # Could be enhanced by scraping article content
                    })
        
        return articles
        
    except Exception as e:
        print(f"Error scraping articles: {e}")
        return []

def generate_rss_feed(articles, author_name, author_url):
    """Generate an RSS feed from the articles"""
    
    # Create RSS structure
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
    # Channel metadata
    ET.SubElement(channel, "title").text = f"Articles by {author_name} - Liberation.fr"
    ET.SubElement(channel, "link").text = author_url
    ET.SubElement(channel, "description").text = f"Latest articles by {author_name} from Liberation.fr"
    ET.SubElement(channel, "language").text = "fr-FR"
    ET.SubElement(channel, "lastBuildDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Add articles as items
    for article in articles:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = article['title']
        ET.SubElement(item, "link").text = article['url']
        ET.SubElement(item, "description").text = article['description']
        ET.SubElement(item, "guid").text = article['url']
        ET.SubElement(item, "pubDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    return ET.tostring(rss, encoding='unicode', method='xml')

def main():
    author_url = "https://www.liberation.fr/auteur/benjamin-delille/"
    author_name = "Benjamin Delille"
    
    print(f"Scraping articles from: {author_url}")
    articles = scrape_author_articles(author_url)
    
    if articles:
        print(f"Found {len(articles)} articles:")
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article['title']}")
        
        # Generate RSS feed
        rss_content = generate_rss_feed(articles, author_name, author_url)
        
        # Save to file
        output_file = "benjamin_delille_rss.xml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(rss_content)
        
        print(f"\nRSS feed generated: {output_file}")
        print("You can use this file with any RSS reader.")
        
    else:
        print("No articles found. The page structure might have changed.")

if __name__ == "__main__":
    main()

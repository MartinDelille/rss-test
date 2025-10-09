#!/usr/bin/env python3
"""
Improved RSS feed generator for Liberation.fr authors
"""

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def extract_date_from_url(url):
    """Extract date from Liberation.fr URL pattern (YYYYMMDD)"""
    # Look for pattern like 20250614 in the URL
    date_match = re.search(r'(\d{8})', url)
    if date_match:
        date_str = date_match.group(1)
        try:
            # Parse the date string (YYYYMMDD)
            year = int(date_str[:4])
            month = int(date_str[4:6])
            day = int(date_str[6:8])
            
            # Create datetime object
            article_date = datetime(year, month, day, 12, 0, 0)  # Use noon as default time
            
            # Format for RSS (RFC 822 format)
            return article_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
        except (ValueError, IndexError):
            pass
    
    # Fallback to current date if no date found in URL
    return datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

def clean_article_title(raw_title):
    """Clean article title by removing date and subscription indicators"""
    if not raw_title:
        return ""
    
    title = raw_title.strip()
    
    # Remove "Abonnés" at the end
    title = re.sub(r'\s*Abonnés\s*$', '', title, flags=re.IGNORECASE)
    
    # Remove French date patterns at the end (like "19 août 2025", "1er juil. 2025", "15 juin 2025")
    # Pattern for French dates: day + month + year
    french_months = [
        'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
        'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre',
        'janv\.?', 'févr\.?', 'mars', 'avr\.?', 'mai', 'juin',
        'juil\.?', 'août', 'sept\.?', 'oct\.?', 'nov\.?', 'déc\.?'
    ]
    
    # Create pattern for French dates
    months_pattern = '|'.join(french_months)
    date_pattern = rf'\s*\d{{1,2}}(?:er)?\s+(?:{months_pattern})\s+\d{{4}}\s*$'
    title = re.sub(date_pattern, '', title, flags=re.IGNORECASE)
    
    # Remove any trailing whitespace and punctuation
    title = title.strip().rstrip('.,;:')
    
    return title

def extract_article_description(article_url):
    """Extract article description/summary from the article page"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(article_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try different methods to extract description
        description = None
        
        # Method 1: Look for meta description
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            description = meta_desc.get('content').strip()
        
        # Method 2: Look for Open Graph description
        if not description:
            og_desc = soup.find('meta', {'property': 'og:description'})
            if og_desc and og_desc.get('content'):
                description = og_desc.get('content').strip()
        
        # Method 3: Look for article lead/summary (common selectors)
        if not description:
            selectors_to_try = [
                '.article-lead',
                '.article-summary', 
                '.lead',
                '.summary',
                '.intro',
                '.article-intro',
                'p.lead',
                '.article-content p:first-of-type',
                '.content p:first-of-type'
            ]
            
            for selector in selectors_to_try:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text(strip=True)
                    if text and len(text) > 50:  # Make sure it's substantial
                        description = text
                        break
        
        # Method 4: Fallback to first substantial paragraph in article
        if not description:
            paragraphs = soup.select('article p, .article p, .content p, main p')
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text and len(text) > 100:  # Look for substantial content
                    description = text
                    break
        
        # Clean and limit description
        if description:
            # Remove excessive whitespace
            description = re.sub(r'\s+', ' ', description)
            # Limit length
            if len(description) > 500:
                description = description[:497] + "..."
            return description
        
        return "Description non disponible"
        
    except Exception as e:
        print(f"  Warning: Could not extract description from {article_url}: {e}")
        return "Description non disponible"

def scrape_author_articles(author_url):
    """Scrape articles from an author's page with improved parsing"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(author_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        print("Analyzing page structure...")
        
        # Try different selectors that might contain articles
        selectors_to_try = [
            'a[href*="/20"]',  # Links containing year (like /2025/)
            'a[href*="liberation.fr"]',  # Liberation.fr links
            'h2 a', 'h3 a',  # Headlines with links
            '.article-link', '.headline a',  # Common CSS classes
            'a[href*="/article"]', 'a[href*="/politique"]', 'a[href*="/international"]'
        ]
        
        for selector in selectors_to_try:
            links = soup.select(selector)
            print(f"Selector '{selector}': found {len(links)} links")
            
            for link in links[:15]:  # Limit to avoid too much output
                href = link.get('href', '')
                raw_title = link.get_text(strip=True)
                
                # Clean the title by removing dates and "Abonnés"
                title = clean_article_title(raw_title)
                
                # Skip if it's not an article URL or has no meaningful title
                if (href and title and len(title) > 15 and 
                    any(pattern in href for pattern in ['/2024/', '/2025/', '/international/', '/politique/'])):
                    
                    # Make sure it's a full URL
                    if href.startswith('/'):
                        full_url = urljoin('https://www.liberation.fr', href)
                    else:
                        full_url = href
                    
                    # Avoid duplicates
                    if not any(art['url'] == full_url for art in articles):
                        pub_date = extract_date_from_url(full_url)
                        print(f"  Found article: {title[:80]}...")
                        print(f"    Extracting description from: {full_url}")
                        
                        # Extract description from the article page
                        description = extract_article_description(full_url)
                        
                        articles.append({
                            'title': title[:200],  # Truncate very long titles
                            'url': full_url,
                            'description': description,
                            'pubDate': pub_date
                        })
            
            if articles:
                break  # Stop if we found articles with this selector
        
        # Remove duplicates and sort by title length (longer titles are usually better)
        unique_articles = []
        seen_urls = set()
        for article in sorted(articles, key=lambda x: len(x['title']), reverse=True):
            if article['url'] not in seen_urls:
                unique_articles.append(article)
                seen_urls.add(article['url'])
        
        return unique_articles[:10]  # Return top 10 articles
        
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
    ET.SubElement(channel, "generator").text = "Custom Liberation.fr RSS Generator"
    
    # Add articles as items
    for article in articles:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = article['title']
        ET.SubElement(item, "link").text = article['url']
        ET.SubElement(item, "description").text = article['description']
        ET.SubElement(item, "guid").text = article['url']
        ET.SubElement(item, "pubDate").text = article['pubDate']
    
    # Format the XML with proper indentation
    ET.indent(rss, space="  ", level=0)
    return ET.tostring(rss, encoding='unicode', method='xml')

def main():
    author_url = "https://www.liberation.fr/auteur/benjamin-delille/"
    author_name = "Benjamin Delille"
    
    print(f"Scraping articles from: {author_url}")
    print("=" * 60)
    
    articles = scrape_author_articles(author_url)
    
    if articles:
        print(f"\nFound {len(articles)} articles:")
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article['title']}")
            print(f"   URL: {article['url']}\n")
        
        # Generate RSS feed
        rss_content = generate_rss_feed(articles, author_name, author_url)
        
        # Save to file
        output_file = "benjamin_delille_rss.xml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(rss_content)
        
        print(f"RSS feed generated: {output_file}")
        print("You can use this file with any RSS reader or serve it from a web server.")
        
        # Show a sample of the RSS content
        print("\nSample RSS content:")
        print("-" * 40)
        print(rss_content[:500] + "...")
        
    else:
        print("No articles found. You might need to manually inspect the page structure.")
        print("Try visiting the author page in a browser to see the current layout.")

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin
import time

# Complete sustainability keywords in Danish
SUSTAINABILITY_KEYWORDS = [
    'bæredygtig', 'bæredygtighed', 'klima', 'miljø', 'genbrug', 'affald', 'madspild',
    'energibesparelse', 'grøn', 'grønt', 'økologi', 'cykel', 'løb', 'ren', 'natur',
    'plante', 'træ', 'skov', 'have', 'frugt', 'grøntsag', 'dyrevelfærd', 'fairtrade',
    'økologisk', 'co2', 'bæredygtig udvikling', 'miljøvenlig', 'bæredygtig livsstil',
    'zero waste', 'plastikfri', 'bæredygtig mode', 'bæredygtig mad', 'bæredygtig transport',
    'bæredygtig by', 'bæredygtig energi', 'bæredygtig turisme', 'bæredygtig design',
    'bæredygtig innovation', 'bæredygtigt forbrug', 'bæredygtigt landbrug', 'bæredygtig skovbrug',
    'bæredygtig fiskeri', 'bæredygtig minedrift', 'bæredygtig vand', 'bæredygtig luft',
    'bæredygtig sundhed', 'bæredygtig uddannelse', 'bæredygtig økonomi', 'bæredygtig ledelse',
    'bæredygtig teknologi', 'bæredygtig arkitektur', 'bæredygtig byggeri', 'bæredygtig bolig',
    'bæredygtig park', 'bæredygtig gade', 'bæredygtig byrum', 'bæredygtig mobilitet',
    'bæredygtig logistik', 'bæredygtig emballage', 'bæredygtig forpackning', 'bæredygtig indkøb',
    'bæredygtig leverandør', 'bæredygtig virksomhed', 'bæredygtig investering', 'bæredygtig finansiering',
    'bæredygtig bank', 'bæredygtig forsikring', 'bæredygtig pension', 'bæredygtig fond',
    'bæredygtig ngo', 'bæredygtig forening', 'bæredygtig frivillig', 'bæredygtig event',
    'bæredygtig festival', 'bæredygtig koncert', 'bæredygtig teater', 'bæredygtig film',
    'bæredygtig kunst', 'bæredygtig musik', 'bæredygtig sport', 'bæredygtig træning',
    'bæredygtig kost', 'bæredygtig slank', 'bæredygtig sundhed', 'bæredygtig wellness',
    'bæredygtig spa', 'bæredygtig ferie', 'bæredygtig rejse', 'bæredygtig turist',
    'bæredygtig oplevelse', 'bæredygtig shopping',
    # Additional from PDF
    'repair', 'reparation', 'løb', 'vandring', 'workshop', 'kursus', 'foredrag',
    'oprydning', 'clean-up', 'beach clean', 'plantning', 'dyrkning', 'læring',
    'undervisning', 'swap', 'bytte', 'fællesspisning', 'madlavning', 'genbrugsmarked',
    'loppemarked', 'brugt', 'secondhand', 'vintage', 'bæredygtigt', 'klimavenlig'
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def contains_sustainability_keywords(text):
    """Check if text contains sustainability keywords."""
    if not text:
        return False
    
    text_lower = text.lower()
    
    # Check for all sustainability keywords
    for keyword in SUSTAINABILITY_KEYWORDS:
        if keyword.lower() in text_lower:
            return True
    
    return False

def scrape_migogaarhus():
    """Scrape events from migogaarhus.dk/kalender/"""
    events = []
    url = "https://migogaarhus.dk/kalender/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for event listings - adjust based on actual structure
        event_items = soup.select('article, .event-item, .post, .item')
        
        for item in event_items[:20]:
            try:
                title_elem = item.select_one('h2, h3, .title, .event-title')
                link_elem = item.select_one('a[href]')
                
                if not title_elem or not link_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = link_elem['href']
                if not link.startswith('http'):
                    link = urljoin('https://migogaarhus.dk', link)
                
                # Try to get description
                description_elem = item.select_one('.description, .excerpt, .content, p')
                description = description_elem.get_text(strip=True)[:300] if description_elem else ""
                
                # Try to get date
                date_elem = item.select_one('.date, .event-date, .post-date, time')
                date_text = date_elem.get_text(strip=True) if date_elem else ""
                
                # Try to get location
                location_elem = item.select_one('.location, .venue, .place')
                location = location_elem.get_text(strip=True) if location_elem else "Aarhus"
                
                if contains_sustainability_keywords(f"{title} {description}"):
                    event = {
                        'title': title,
                        'description': description,
                        'date': date_text,
                        'time': '',
                        'location': location,
                        'address': location,
                        'link': link,
                        'source': 'migogaarhus.dk',
                        'category': 'event',
                        'image': '',
                        'organizer': '',
                        'points': 100
                    }
                    events.append(event)
                    
            except Exception as e:
                print(f"Error parsing event from migogaarhus: {e}")
                continue
                
    except Exception as e:
        print(f"Error scraping migogaarhus: {e}")
    
    return events

def scrape_tipaarhus():
    """Scrape events from tipaarhus.dk/det-sker-i-aarhus/"""
    events = []
    url = "https://tipaarhus.dk/det-sker-i-aarhus/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        event_items = soup.select('article, .post, .event, .arrangement')
        
        for item in event_items[:20]:
            try:
                title_elem = item.select_one('h2, h3, .entry-title, .title')
                link_elem = title_elem.select_one('a') if title_elem else item.select_one('a[href]')
                
                if not title_elem or not link_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = link_elem['href']
                if not link.startswith('http'):
                    link = urljoin('https://tipaarhus.dk', link)
                
                description_elem = item.select_one('.entry-content, .excerpt, .description')
                description = description_elem.get_text(strip=True)[:300] if description_elem else ""
                
                date_elem = item.select_one('.date, .post-date, .event-date')
                date_text = date_elem.get_text(strip=True) if date_elem else ""
                
                location_elem = item.select_one('.location, .venue')
                location = location_elem.get_text(strip=True) if location_elem else "Aarhus"
                
                if contains_sustainability_keywords(f"{title} {description}"):
                    event = {
                        'title': title,
                        'description': description,
                        'date': date_text,
                        'time': '',
                        'location': location,
                        'address': location,
                        'link': link,
                        'source': 'tipaarhus.dk',
                        'category': 'event',
                        'image': '',
                        'organizer': '',
                        'points': 100
                    }
                    events.append(event)
                    
            except Exception as e:
                print(f"Error parsing event from tipaarhus: {e}")
                continue
                
    except Exception as e:
        print(f"Error scraping tipaarhus: {e}")
    
    return events

def scrape_visitaarhus():
    """Scrape events from visitaarhus.dk sustainability page"""
    events = []
    url = "https://www.visitaarhus.dk/aarhusregionen/baeredygtighed-i-fokus"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # This page should have sustainability content
        content_items = soup.select('article, .content-item, .news-item, .card')
        
        for item in content_items[:15]:
            try:
                title_elem = item.select_one('h2, h3, h4, .title')
                link_elem = item.select_one('a[href]')
                
                if not title_elem or not link_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = link_elem['href']
                if not link.startswith('http'):
                    link = urljoin('https://www.visitaarhus.dk', link)
                
                description_elem = item.select_one('p, .description, .text')
                description = description_elem.get_text(strip=True)[:300] if description_elem else ""
                
                # This page is about sustainability, so include relevant content
                if contains_sustainability_keywords(f"{title} {description}"):
                    event = {
                        'title': title,
                        'description': description,
                        'date': 'Se link for dato',
                        'time': '',
                        'location': 'Aarhus region',
                        'address': '',
                        'link': link,
                        'source': 'visitaarhus.dk',
                        'category': 'sustainability',
                        'image': '',
                        'organizer': '',
                        'points': 100
                    }
                    events.append(event)
                    
            except Exception as e:
                print(f"Error parsing content from visitaarhus: {e}")
                continue
                
    except Exception as e:
        print(f"Error scraping visitaarhus: {e}")
    
    return events

def scrape_aarhusliv():
    """Scrape events from aarhusliv.dk"""
    events = []
    url = "https://aarhusliv.dk/det-sker-i-aarhus/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        event_items = soup.select('article, .post, .event-item, .list-item')
        
        for item in event_items[:25]:
            try:
                title_elem = item.select_one('h2, h3, .entry-title, .title')
                link_elem = title_elem.select_one('a') if title_elem else item.select_one('a[href]')
                
                if not title_elem or not link_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = link_elem['href']
                if not link.startswith('http'):
                    link = urljoin('https://aarhusliv.dk', link)
                
                description_elem = item.select_one('.entry-content, .excerpt, p')
                description = description_elem.get_text(strip=True)[:300] if description_elem else ""
                
                date_elem = item.select_one('.date, .time, .post-date')
                date_text = date_elem.get_text(strip=True) if date_elem else ""
                
                if contains_sustainability_keywords(f"{title} {description}"):
                    event = {
                        'title': title,
                        'description': description,
                        'date': date_text,
                        'time': '',
                        'location': 'Aarhus',
                        'address': '',
                        'link': link,
                        'source': 'aarhusliv.dk',
                        'category': 'event',
                        'image': '',
                        'organizer': '',
                        'points': 100
                    }
                    events.append(event)
                    
            except Exception as e:
                print(f"Error parsing event from aarhusliv: {e}")
                continue
                
    except Exception as e:
        print(f"Error scraping aarhusliv: {e}")
    
    return events

def scrape_aarhusevents():
    """Scrape events from aarhusevents.dk"""
    events = []
    url = "https://aarhusevents.dk/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        event_items = soup.select('.event, .arrangement, article, .item')
        
        for item in event_items[:25]:
            try:
                title_elem = item.select_one('h2, h3, .title, .event-title')
                link_elem = item.select_one('a[href]')
                
                if not title_elem or not link_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = link_elem['href']
                if not link.startswith('http'):
                    link = urljoin('https://aarhusevents.dk', link)
                
                description_elem = item.select_one('.description, .excerpt, .content')
                description = description_elem.get_text(strip=True)[:300] if description_elem else ""
                
                date_elem = item.select_one('.date, .event-date')
                date_text = date_elem.get_text(strip=True) if date_elem else ""
                
                location_elem = item.select_one('.location, .venue')
                location = location_elem.get_text(strip=True) if location_elem else "Aarhus"
                
                if contains_sustainability_keywords(f"{title} {description}"):
                    event = {
                        'title': title,
                        'description': description,
                        'date': date_text,
                        'time': '',
                        'location': location,
                        'address': location,
                        'link': link,
                        'source': 'aarhusevents.dk',
                        'category': 'event',
                        'image': '',
                        'organizer': '',
                        'points': 100
                    }
                    events.append(event)
                    
            except Exception as e:
                print(f"Error parsing event from aarhusevents: {e}")
                continue
                
    except Exception as e:
        print(f"Error scraping aarhusevents: {e}")
    
    return events

def scrape_aarhusinside():
    """Scrape events from aarhusinside.dk"""
    events = []
    url = "https://aarhusinside.dk/oplevelser-i-aarhus/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        event_items = soup.select('article, .post, .experience-item, .listing')
        
        for item in event_items[:25]:
            try:
                title_elem = item.select_one('h2, h3, .entry-title, .title')
                link_elem = title_elem.select_one('a') if title_elem else item.select_one('a[href]')
                
                if not title_elem or not link_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = link_elem['href']
                if not link.startswith('http'):
                    link = urljoin('https://aarhusinside.dk', link)
                
                description_elem = item.select_one('.entry-content, .excerpt, .description')
                description = description_elem.get_text(strip=True)[:300] if description_elem else ""
                
                date_elem = item.select_one('.date, .post-date')
                date_text = date_elem.get_text(strip=True) if date_elem else ""
                
                if contains_sustainability_keywords(f"{title} {description}"):
                    event = {
                        'title': title,
                        'description': description,
                        'date': date_text,
                        'time': '',
                        'location': 'Aarhus',
                        'address': '',
                        'link': link,
                        'source': 'aarhusinside.dk',
                        'category': 'experience',
                        'image': '',
                        'organizer': '',
                        'points': 100
                    }
                    events.append(event)
                    
            except Exception as e:
                print(f"Error parsing event from aarhusinside: {e}")
                continue
                
    except Exception as e:
        print(f"Error scraping aarhusinside: {e}")
    
    return events

def scrape_domen_aarhus():
    """Scrape events from domen.aarhus.dk (Aarhus Kommune)"""
    events = []
    url = "https://domen.aarhus.dk/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find event listings - this site might have a specific structure
        event_items = soup.select('.event, .arrangement, .activity, .item')
        
        for item in event_items[:20]:
            try:
                title_elem = item.select_one('h2, h3, .title, .event-title')
                link_elem = item.select_one('a[href]')
                
                if not title_elem or not link_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = link_elem['href']
                if not link.startswith('http'):
                    link = urljoin('https://domen.aarhus.dk', link)
                
                description_elem = item.select_one('.description, .summary, p')
                description = description_elem.get_text(strip=True)[:300] if description_elem else ""
                
                date_elem = item.select_one('.date, .time')
                date_text = date_elem.get_text(strip=True) if date_elem else ""
                
                location_elem = item.select_one('.location, .place')
                location = location_elem.get_text(strip=True) if location_elem else "Aarhus"
                
                if contains_sustainability_keywords(f"{title} {description}"):
                    event = {
                        'title': title,
                        'description': description,
                        'date': date_text,
                        'time': '',
                        'location': location,
                        'address': '',
                        'link': link,
                        'source': 'domen.aarhus.dk',
                        'category': 'municipal',
                        'image': '',
                        'organizer': 'Aarhus Kommune',
                        'points': 100
                    }
                    events.append(event)
                    
            except Exception as e:
                print(f"Error parsing event from domen.aarhus: {e}")
                continue
                
    except Exception as e:
        print(f"Error scraping domen.aarhus: {e}")
    
    return events

def scrape_klimahuset():
    """Scrape events from Klimahuset Aarhus"""
    events = []
    url = "https://klimahusetaarhus.dk/arrangementer/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        event_items = soup.select('article, .event, .arrangement, .post')
        
        for item in event_items[:20]:
            try:
                title_elem = item.select_one('h2, h3, .entry-title')
                link_elem = title_elem.select_one('a') if title_elem else item.select_one('a[href]')
                
                if not title_elem or not link_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = link_elem['href']
                if not link.startswith('http'):
                    link = urljoin('https://klimahusetaarhus.dk', link)
                
                description_elem = item.select_one('.entry-content, .description, p')
                description = description_elem.get_text(strip=True)[:300] if description_elem else ""
                
                date_elem = item.select_one('.date, .event-date')
                date_text = date_elem.get_text(strip=True) if date_elem else "Kommer snart"
                
                # All Klimahuset events are sustainability-related
                event = {
                    'title': title,
                    'description': description,
                    'date': date_text,
                    'time': '',
                    'location': 'Klimahuset Aarhus',
                    'address': 'Magistrsparken 2, 8000 Aarhus C',
                    'link': link,
                    'source': 'klimahusetaarhus.dk',
                    'category': 'climate',
                    'image': '',
                    'organizer': 'Klimahuset Aarhus',
                    'points': 100
                }
                events.append(event)
                
            except Exception as e:
                print(f"Error parsing event from Klimahuset: {e}")
                continue
                
    except Exception as e:
        print(f"Error scraping Klimahuset: {e}")
    
    return events

def scrape_godsbanen():
    """Scrape events from Godsbanen"""
    events = []
    url = "https://godsbanen.dk/arrangementer"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        event_items = soup.select('.event, .arrangement, article, .post')
        
        for item in event_items[:25]:
            try:
                title_elem = item.select_one('h2, h3, .event-title')
                link_elem = item.select_one('a[href]')
                
                if not title_elem or not link_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = link_elem['href']
                if not link.startswith('http'):
                    link = urljoin('https://godsbanen.dk', link)
                
                description_elem = item.select_one('.description, .excerpt, p')
                description = description_elem.get_text(strip=True)[:300] if description_elem else ""
                
                date_elem = item.select_one('.date, .event-date')
                date_text = date_elem.get_text(strip=True) if date_elem else "Aktiviteter"
                
                if contains_sustainability_keywords(f"{title} {description}"):
                    event = {
                        'title': title,
                        'description': description,
                        'date': date_text,
                        'time': '',
                        'location': 'Godsbanen',
                        'address': 'Skovgaardsgade 3, 8000 Aarhus C',
                        'link': link,
                        'source': 'godsbanen.dk',
                        'category': 'creative',
                        'image': '',
                        'organizer': 'Godsbanen',
                        'points': 100
                    }
                    events.append(event)
                    
            except Exception as e:
                print(f"Error parsing event from Godsbanen: {e}")
                continue
                
    except Exception as e:
        print(f"Error scraping Godsbanen: {e}")
    
    return events

def extract_events_from_pdf():
    """Extract event information from the PDF content"""
    events = []
    
    # These are example events from the PDF (you would need to parse the actual PDF)
    # Since we can't parse the image PDF, I'll create some based on what I see
    
    pdf_based_events = [
        {
            'title': "Queers & Coffee - at Studenterhus Aarhus",
            'description': "Social gathering for the queer community at Studenterhus Aarhus",
            'date': "Today",
            'time': "16:30",
            'location': "Studenterhus Aarhus",
            'address': "",
            'link': "#",
            'source': "Facebook (PDF)",
            'category': "community",
            'image': "",
            'organizer': "Studenterhus Aarhus",
            'points': 80
        },
        {
            'title': "Italiensk Fællesspisning",
            'description': "Italian community dinner and social gathering",
            'date': "Today",
            'time': "17:00",
            'location': "Katrinebjergvej 77K",
            'address': "Katrinebjergvej 77K, Aarhus",
            'link': "#",
            'source': "Facebook (PDF)",
            'category': "food",
            'image': "",
            'organizer': "Local community",
            'points': 80
        },
        {
            'title': "Christmas Karaoke",
            'description': "Christmas karaoke night at Studenterhus Aarhus",
            'date': "Tue, 9 Dec",
            'time': "20:00",
            'location': "Studenterhus Aarhus",
            'address': "",
            'link': "#",
            'source': "Facebook (PDF)",
            'category': "music",
            'image': "",
            'organizer': "Studenterhus Aarhus",
            'points': 60
        },
        {
            'title': "Repair Café Aarhus",
            'description': "Bring broken items and learn to repair them with volunteers",
            'date': "Regular event",
            'time': "Check schedule",
            'location': "Godsbanen",
            'address': "Skovgaardsgade 3, 8000 Aarhus C",
            'link': "https://repaircafeaarhus.dk",
            'source': "Repair Café Aarhus",
            'category': "repair",
            'image': "",
            'organizer': "Repair Café Aarhus",
            'points': 100
        }
    ]
    
    # Filter for sustainability events
    for event in pdf_based_events:
        if contains_sustainability_keywords(f"{event['title']} {event['description']}"):
            events.append(event)
    
    return events

def clean_and_deduplicate_events(events):
    """Clean and remove duplicate events"""
    seen_titles = set()
    cleaned_events = []
    
    for event in events:
        # Clean the title
        title = event['title'].strip()
        title_key = title.lower()
        
        # Skip if we've seen this title before
        if title_key in seen_titles:
            continue
        
        seen_titles.add(title_key)
        
        # Clean other fields
        event['title'] = title
        event['description'] = event['description'].strip() if event['description'] else ""
        
        # Add default values if missing
        if not event.get('location'):
            event['location'] = 'Aarhus'
        if not event.get('category'):
            event['category'] = 'event'
        
        cleaned_events.append(event)
    
    return cleaned_events

def categorize_event(event):
    """Categorize event based on keywords in title and description"""
    text = f"{event['title']} {event['description']}".lower()
    
    categories = []
    
    # Define category keywords
    category_keywords = {
        'cleaning': ['renhold', 'oprydning', 'clean-up', 'skrald', 'affald', 'plastik'],
        'food': ['madspild', 'madlavning', 'fødevare', 'spise', 'måltid', 'fællesspisning'],
        'repair': ['repair', 'reparation', 'fix', 'istandsættelse'],
        'workshop': ['workshop', 'kursus', 'læring', 'undervisning', 'foredrag'],
        'gardening': ['have', 'plante', 'dyrkning', 'gartneri', 'grøntsag', 'frugt'],
        'transport': ['cykel', 'transport', 'mobilitet', 'elbil', 'løb', 'vandring'],
        'energy': ['energi', 'besparelse', 'solcelle', 'vindmølle', 'co2'],
        'community': ['fællesskab', 'forening', 'frivillig', 'samfund', 'community'],
        'swap': ['swap', 'bytte', 'genbrugsmarked', 'loppemarked'],
        'climate': ['klima', 'klimahuset', 'co2', 'opvarmning'],
        'creative': ['kunst', 'design', 'kreativ', 'håndværk']
    }
    
    for category, keywords in category_keywords.items():
        if any(keyword in text for keyword in keywords):
            categories.append(category)
    
    # Add sustainability as default if no specific category found
    if not categories:
        categories.append('sustainability')
    
    event['categories'] = categories
    return event

def main():
    print("🚀 Starting Aarhus Sustainability Events Scraper...")
    print("=" * 50)
    
    all_events = []
    
    # Scrape from all websites
    sources = [
        ("migogaarhus.dk", scrape_migogaarhus),
        ("tipaarhus.dk", scrape_tipaarhus),
        ("visitaarhus.dk", scrape_visitaarhus),
        ("aarhusliv.dk", scrape_aarhusliv),
        ("aarhusevents.dk", scrape_aarhusevents),
        ("aarhusinside.dk", scrape_aarhusinside),
        ("domen.aarhus.dk", scrape_domen_aarhus),
        ("klimahusetaarhus.dk", scrape_klimahuset),
        ("godsbanen.dk", scrape_godsbanen),
    ]
    
    for source_name, scraper_func in sources:
        print(f"📡 Scraping {source_name}...")
        try:
            events = scraper_func()
            all_events.extend(events)
            print(f"   Found {len(events)} events")
        except Exception as e:
            print(f"   Error: {e}")
        time.sleep(1)  # Be polite to servers
    
    print("=" * 50)
    
    # Add events from PDF analysis
    print("📄 Adding events from PDF analysis...")
    pdf_events = extract_events_from_pdf()
    all_events.extend(pdf_events)
    print(f"   Added {len(pdf_events)} events from PDF")
    
    # Clean and deduplicate
    print("🧹 Cleaning and deduplicating events...")
    cleaned_events = clean_and_deduplicate_events(all_events)
    
    # Categorize events
    print("🏷️ Categorizing events...")
    categorized_events = []
    for event in cleaned_events:
        categorized_events.append(categorize_event(event))
    
    # Sort by date (put events with actual dates first)
    def sort_key(event):
        date_text = event.get('date', '').lower()
        if 'i dag' in date_text or 'today' in date_text:
            return (0, date_text)
        elif 'i morgen' in date_text or 'tomorrow' in date_text:
            return (1, date_text)
        else:
            return (2, date_text)
    
    categorized_events.sort(key=sort_key)
    
    # Limit to max 15 events
    final_events = categorized_events[:15]
    
    # Create output structure
    output = {
        'metadata': {
            'last_updated': datetime.now().isoformat(),
            'total_events': len(final_events),
            'sources': [source[0] for source in sources] + ['Facebook (PDF analysis)']
        },
        'events': final_events
    }
    
    # Save to JSON file
    with open('aarhus_sustainability_events.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("=" * 50)
    print(f"✅ Successfully scraped {len(final_events)} sustainability events!")
    print(f"📁 Saved to 'aarhus_sustainability_events.json'")
    
    # Print summary
    print("\n📊 Summary by category:")
    categories_count = {}
    for event in final_events:
        for category in event['categories']:
            categories_count[category] = categories_count.get(category, 0) + 1
    
    for category, count in sorted(categories_count.items()):
        print(f"  {category}: {count} events")
    
    print("\n🌱 Ready to use in your static website!")

if __name__ == "__main__":
    main()
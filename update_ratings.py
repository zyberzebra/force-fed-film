import json
import feedparser
import re
from datetime import datetime

# RSS Feed URLs
FEEDS = {
    'derschaki': 'https://letterboxd.com/derschaki/rss/',
    'zebrastuhl': 'https://letterboxd.com/zebrastuhl/rss/'  # Anpassen
}

def parse_rating_from_title(title):
    """Extrahiert Rating aus dem Titel (z.B. '★★★½' -> 3.5)"""
    match = re.search(r'★+½?', title)
    if not match:
        return None
    
    stars = match.group()
    full_stars = stars.count('★')
    half_star = 0.5 if '½' in stars else 0
    return full_stars + half_star

def normalize_title(title):
    """Normalisiert Filmtitel für Vergleich"""
    # Entfernt Jahr und Rating aus dem Titel
    title = re.sub(r',\s*\d{4}\s*-\s*★.*$', '', title)
    return title.strip().lower()

def fetch_ratings():
    """Holt Bewertungen aus beiden RSS-Feeds"""
    all_ratings = {}
    
    for user, feed_url in FEEDS.items():
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries:
            title = normalize_title(entry.title)
            rating = parse_rating_from_title(entry.title)
            
            if title not in all_ratings:
                all_ratings[title] = {}
            
            all_ratings[title][user] = {
                'rating': rating,
                'url': entry.link
            }
    
    return all_ratings

def update_films_json():
    """Aktualisiert films.json mit neuen Ratings"""
    with open('films.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    ratings = fetch_ratings()
    updated = False
    
    # Update current film
    current_title = normalize_title(f"{data['currentFilm']['title']}, {data['currentFilm']['year']}")
    if current_title in ratings:
        for user in ['derschaki', 'zebrastuhl']:
            if user in ratings[current_title]:
                data['currentFilm'][user]['rating'] = ratings[current_title][user]['rating']
                data['currentFilm'][user]['letterboxdUrl'] = ratings[current_title][user]['url']
                updated = True
    
    # Update past films
    for film in data['pastFilms']:
        film_title = normalize_title(f"{film['title']}, {film['year']}")
        if film_title in ratings:
            for user in ['derschaki', 'zebrastuhl']:
                if user in ratings[film_title]:
                    film[user]['rating'] = ratings[film_title][user]['rating']
                    film[user]['letterboxdUrl'] = ratings[film_title][user]['url']
                    updated = True
    
    if updated:
        with open('films.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("✅ Ratings updated successfully")
    else:
        print("ℹ️ No updates found")

if __name__ == '__main__':
    update_films_json()

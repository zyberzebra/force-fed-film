import json
import feedparser
import re

# RSS Feed URLs
FEEDS = {
    'derschaki': 'https://letterboxd.com/derschaki/rss/',
    'zebrastuhl': 'https://letterboxd.com/zebrastuhl/rss/'  # Anpassen mit korrektem Username
}

def parse_rating_from_entry(entry):
    """Extrahiert Rating aus dem Letterboxd RSS Entry"""
    # Versuche aus memberRating zu lesen
    if hasattr(entry, 'letterboxd_memberrating'):
        try:
            return float(entry.letterboxd_memberrating)
        except:
            pass
    
    # Fallback: Parse aus Titel
    match = re.search(r'★+½?', entry.title)
    if not match:
        return None
    
    stars = match.group()
    full_stars = stars.count('★')
    half_star = 0.5 if '½' in stars else 0
    return full_stars + half_star

def extract_slug_from_url(url):
    """Extrahiert Slug aus Letterboxd URL"""
    # https://letterboxd.com/derschaki/film/boiling-point-2021/ -> boiling-point-2021
    match = re.search(r'/film/([^/]+)/', url)
    return match.group(1) if match else None

def normalize_slug(slug):
    """Normalisiert Slug für Vergleich"""
    return slug.lower().strip()

def fetch_ratings():
    """Holt Bewertungen aus beiden RSS-Feeds"""
    all_ratings = {}
    
    for user, feed_url in FEEDS.items():
        print(f"📡 Fetching {user}'s feed...")
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries:
            slug = extract_slug_from_url(entry.link)
            if not slug:
                continue
            
            slug_normalized = normalize_slug(slug)
            rating = parse_rating_from_entry(entry)
            
            if slug_normalized not in all_ratings:
                all_ratings[slug_normalized] = {}
            
            all_ratings[slug_normalized][user] = {
                'rating': rating,
                'slug': slug  # Original slug mit korrekter Schreibweise
            }
            
            print(f"  ✓ Found: {slug} - {rating}★")
    
    return all_ratings

def update_films_json():
    """Aktualisiert films.json mit neuen Ratings"""
    with open('films.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    ratings = fetch_ratings()
    updated = False
    
    # Update current film
    current_slug = normalize_slug(data['currentFilm']['letterboxdSlug'])
    if current_slug in ratings:
        print(f"\n🎬 Updating current film: {data['currentFilm']['title']}")
        for user in ['derschaki', 'zebrastuhl']:
            if user in ratings[current_slug] and ratings[current_slug][user]['rating']:
                old_rating = data['currentFilm'][user]['rating']
                new_rating = ratings[current_slug][user]['rating']
                data['currentFilm'][user]['rating'] = new_rating
                print(f"  {user}: {old_rating} → {new_rating}★")
                updated = True
    
    # Update past films
    for film in data['pastFilms']:
        film_slug = normalize_slug(film['letterboxdSlug'])
        if film_slug in ratings:
            print(f"\n🎬 Updating: {film['title']}")
            for user in ['derschaki', 'zebrastuhl']:
                if user in ratings[film_slug] and ratings[film_slug][user]['rating']:
                    old_rating = film[user]['rating']
                    new_rating = ratings[film_slug][user]['rating']
                    if old_rating != new_rating:
                        film[user]['rating'] = new_rating
                        print(f"  {user}: {old_rating} → {new_rating}★")
                        updated = True
    
    if updated:
        with open('films.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("\n✅ Ratings updated successfully!")
    else:
        print("\nℹ️  No updates found")

if __name__ == '__main__':
    update_films_json()

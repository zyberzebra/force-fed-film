import json
import feedparser
import re
from bs4 import BeautifulSoup

# RSS Feed URLs
FEEDS = {
    'derschaki': 'https://letterboxd.com/derschaki/rss/',
    'zebrastuhl': 'https://letterboxd.com/zebrastuhl/rss/'
}

def extract_review_text(description):
    """Extrahiert Review-Text aus HTML Description"""
    if not description:
        return None
    
    soup = BeautifulSoup(description, 'html.parser')
    
    for img in soup.find_all('img'):
        img.decompose()
    
    text = soup.get_text(separator='\n').strip()
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    text = '\n'.join(lines)
    
    return text if text else None

def extract_poster_url(description):
    """Extrahiert Poster-URL aus Description"""
    if not description:
        return None
    
    match = re.search(r'<img src="(https://a\.ltrbxd\.com/[^"]+)"', description)
    return match.group(1) if match else None

def parse_rating_from_entry(entry):
    """Extrahiert Rating aus dem Letterboxd RSS Entry"""
    if hasattr(entry, 'letterboxd_memberrating'):
        try:
            return float(entry.letterboxd_memberrating)
        except:
            pass
    
    match = re.search(r'★+½?', entry.title)
    if not match:
        return None
    
    stars = match.group()
    full_stars = stars.count('★')
    half_star = 0.5 if '½' in stars else 0
    return full_stars + half_star

def extract_slug_from_url(url):
    """Extrahiert Slug aus Letterboxd URL"""
    match = re.search(r'/film/([^/]+)/', url)
    return match.group(1) if match else None

def normalize_slug(slug):
    """Normalisiert Slug für Vergleich"""
    return slug.lower().strip()

def fetch_ratings():
    """Holt alle Daten aus beiden RSS-Feeds"""
    all_data = {}
    
    for user, feed_url in FEEDS.items():
        print(f"📡 Fetching {user}'s feed...")
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries:
            slug = extract_slug_from_url(entry.link)
            if not slug:
                continue
            
            slug_normalized = normalize_slug(slug)
            rating = parse_rating_from_entry(entry)
            review = extract_review_text(entry.get('description', ''))
            poster = extract_poster_url(entry.get('description', ''))
            
            watched_date = getattr(entry, 'letterboxd_watcheddate', None)
            is_rewatch = getattr(entry, 'letterboxd_rewatch', 'No') == 'Yes'
            film_title = getattr(entry, 'letterboxd_filmtitle', None)
            film_year = getattr(entry, 'letterboxd_filmyear', None)
            tmdb_id = getattr(entry, 'tmdb_movieid', None)
            
            if slug_normalized not in all_data:
                all_data[slug_normalized] = {
                    'slug': slug,
                    'title': film_title,
                    'year': film_year,
                    'tmdbId': tmdb_id,
                    'posterUrl': poster,
                    'users': {}
                }
            
            if poster and not all_data[slug_normalized]['posterUrl']:
                all_data[slug_normalized]['posterUrl'] = poster
            
            all_data[slug_normalized]['users'][user] = {
                'rating': rating,
                'watchedDate': watched_date,
                'review': review,
                'isRewatch': is_rewatch
            }
            
            print(f"  ✓ {slug}: {rating}★ | Review: {'Yes' if review else 'No'}")
    
    return all_data

def update_films_json():
    """Aktualisiert films.json mit allen Daten aus RSS"""
    with open('films.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    rss_data = fetch_ratings()
    updated = False
    
    current_slug = normalize_slug(data['currentFilm']['letterboxdSlug'])
    if current_slug in rss_data:
        print(f"\n🎬 Updating current film: {data['currentFilm']['title']}")
        film_data = rss_data[current_slug]
        
        if film_data.get('tmdbId') and not data['currentFilm'].get('tmdbId'):
            data['currentFilm']['tmdbId'] = film_data['tmdbId']
            updated = True
        
        if film_data.get('posterUrl') and not data['currentFilm'].get('posterUrl'):
            data['currentFilm']['posterUrl'] = film_data['posterUrl']
            updated = True
        
        for user in ['derschaki', 'zebrastuhl']:
            if user in film_data['users']:
                user_data = film_data['users'][user]
                
                if user_data['rating']:
                    data['currentFilm'][user]['rating'] = user_data['rating']
                    updated = True
                
                if user_data['watchedDate']:
                    data['currentFilm'][user]['watchedDate'] = user_data['watchedDate']
                    updated = True
                
                if user_data['review']:
                    data['currentFilm'][user]['review'] = user_data['review']
                    updated = True
                
                data['currentFilm'][user]['isRewatch'] = user_data['isRewatch']
                
                print(f"  {user}: {user_data['rating']}★ | Watched: {user_data['watchedDate']}")
    
    for film in data['pastFilms']:
        film_slug = normalize_slug(film['letterboxdSlug'])
        if film_slug in rss_data:
            print(f"\n🎬 Updating: {film['title']}")
            film_data = rss_data[film_slug]
            
            if film_data.get('tmdbId') and not film.get('tmdbId'):
                film['tmdbId'] = film_data['tmdbId']
                updated = True
            
            if film_data.get('posterUrl') and not film.get('posterUrl'):
                film['posterUrl'] = film_data['posterUrl']
                updated = True
            
            for user in ['derschaki', 'zebrastuhl']:
                if user in film_data['users']:
                    user_data = film_data['users'][user]
                    
                    if user_data['rating'] and film[user]['rating'] != user_data['rating']:
                        film[user]['rating'] = user_data['rating']
                        updated = True
                    
                    if user_data['watchedDate']:
                        film[user]['watchedDate'] = user_data['watchedDate']
                        updated = True
                    
                    if user_data['review']:
                        film[user]['review'] = user_data['review']
                        updated = True
                    
                    film[user]['isRewatch'] = user_data['isRewatch']
                    
                    print(f"  {user}: {user_data['rating']}★")
    
    if updated:
        with open('films.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("\n✅ Data updated successfully!")
    else:
        print("\nℹ️  No updates found")

if __name__ == '__main__':
    update_films_json()

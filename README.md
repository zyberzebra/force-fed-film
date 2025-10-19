# 🎬 Force Fed Film Club

A minimalist film club tracker built with vanilla HTML/CSS/JavaScript and hosted on GitHub Pages. Automatically syncs ratings and reviews from Letterboxd RSS feeds.

![Force Fed Film Club](https://img.shields.io/badge/films-tracked-ff6b6b)
![GitHub Pages](https://img.shields.io/badge/deployed-github%20pages-00d735)

## 📖 Overview

**Force Fed Film Club** is a simple website for tracking film club viewings between two members. The site displays:

- **Current Film**: The upcoming movie to watch (with deadline)
- **Past Films**: Complete viewing history with ratings and reviews
- **Letterboxd Integration**: Automatic sync of ratings, reviews, and watch dates

## ✨ Features

- 🎯 **Minimal Dependencies**: Pure HTML, CSS, JavaScript (no frameworks)
- 🌙 **Dark Cinematic Theme**: Inspired by Letterboxd's aesthetic
- 🔄 **Auto-Sync**: Daily GitHub Action fetches ratings from Letterboxd RSS
- 📱 **Responsive Design**: Works on mobile and desktop
- ⭐ **Star Ratings**: Visual 0.5-5 star display with half-star support
- 📝 **Review Display**: Shows Letterboxd review text and watch dates
- 🔁 **Rewatch Detection**: Badges for rewatched films

## 🚀 Quick Start

### 1. Fork/Clone This Repository

```bash
git clone https://github.com/YOUR-USERNAME/force-fed-film-club.git
cd force-fed-film-club
```

### 2. Update Configuration

Edit `update_ratings.py` with your Letterboxd usernames:

```python
FEEDS = {
    'derschaki': 'https://letterboxd.com/derschaki/rss/',
    'zebrastuhl': 'https://letterboxd.com/zebrastuhl/rss/'  # Change this
}
```

### 3. Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Set **Source** to `main` branch
3. Save

Your site will be live at: `https://YOUR-USERNAME.github.io/force-fed-film-club/`

### 4. Enable GitHub Actions

The workflow runs automatically once you push to `main`. It will:
- Fetch both Letterboxd RSS feeds daily at 2 AM
- Extract ratings, reviews, watch dates, and poster URLs
- Create a Pull Request with updates

## 📁 Project Structure

```
force-fed-film-club/
├── index.html              # Main HTML structure
├── style.css               # Dark cinematic styling
├── script.js               # Client-side JavaScript
├── films.json              # Film data (you edit this)
├── update_ratings.py       # RSS sync script
├── requirements.txt        # Python dependencies
└── .github/
    └── workflows/
        └── update-ratings.yml  # GitHub Action
```

## 🎬 Managing Films

### Adding a New "Current Film"

When you decide on the next film, **manually edit** `films.json`:

#### Before:
```json
{
  "currentFilm": {
    "title": "The Outrun",
    "year": 2024,
    "clubDate": "2025-11-01",
    "letterboxdSlug": "the-outrun"
  },
  "pastFilms": []
}
```

#### After:
```json
{
  "currentFilm": {
    "title": "Anora",
    "year": 2024,
    "clubDate": "2025-11-15",
    "letterboxdSlug": "anora",
    "tmdbId": null,
    "posterUrl": null,
    "derschaki": {
      "rating": null,
      "watchedDate": null,
      "review": null,
      "isRewatch": false
    },
    "zebrastuhl": {
      "rating": null,
      "watchedDate": null,
      "review": null,
      "isRewatch": false
    }
  },
  "pastFilms": [
    {
      "title": "The Outrun",
      "year": 2024,
      "clubDate": "2025-11-01",
      "letterboxdSlug": "the-outrun"
    }
  ]
}
```

### Finding the Letterboxd Slug

The slug is the film identifier in the Letterboxd URL:

```
https://letterboxd.com/film/the-outrun/
                            ^^^^^^^^^^
                            This is the slug
```

Use this **exact slug** in your JSON (lowercase, with hyphens).

## 🤖 How Auto-Sync Works

1. **GitHub Action** runs daily at 2 AM (or manually via "Actions" tab)
2. **Python script** fetches both RSS feeds
3. **Matches films** by comparing `letterboxdSlug` to RSS URLs
4. **Extracts data**:
   - Rating (0.5-5 stars)
   - Review text (from HTML description)
   - Watch date
   - Rewatch status
   - Poster URL (from embedded image)
5. **Updates** `films.json` with new data
6. **Creates Pull Request** for you to review and merge

## 📋 Manual Tasks

You must manually:

1. ✅ **Choose the next film** and add it to `films.json`
2. ✅ **Set the club date** (deadline for watching)
3. ✅ **Move finished films** from `currentFilm` to `pastFilms`
4. ✅ **Merge Pull Requests** from the auto-sync action

The script handles:

- ✅ Fetching ratings from Letterboxd
- ✅ Extracting reviews
- ✅ Recording watch dates
- ✅ Downloading poster URLs

## 🛠️ Development

### Running Locally

```bash
# Serve with any static server
python -m http.server 8000

# Or use VS Code Live Server extension
```

Open `http://localhost:8000`

### Testing RSS Sync

```bash
# Install dependencies
pip install -r requirements.txt

# Run sync script
python update_ratings.py
```

### Manual Workflow Trigger

1. Go to **Actions** tab
2. Select "Update Film Ratings"
3. Click "Run workflow"

## 🎨 Customization

### Changing Colors

Edit `style.css`:

```css
/* Main background gradient */
background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);

/* Accent color (links, borders) */
color: #ff6b6b;  /* Change this */

/* Letterboxd link color */
.letterboxd-link { color: #00d735; }
```

### Adjusting Compactness

Reduce padding in `style.css`:

```css
.film-card {
  padding: 0.8rem;  /* Make smaller */
}
```

## 📦 Dependencies

**Client-side:** None (vanilla JS)

**Server-side (GitHub Action):**
- Python 3.10+
- `feedparser==6.0.10` - RSS parsing
- `beautifulsoup4==4.12.2` - HTML/review text extraction

## 🤝 Contributing

This is a personal film club tracker, but feel free to fork and adapt for your own use!

## 📄 License

MIT License - Do whatever you want with it!

## 👥 Credits

Created by **derschaki** & **zebrastuhl** for Force Fed Film Club.

---

**Enjoy tracking your film club! 🍿**

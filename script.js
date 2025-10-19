async function loadFilms() {
    try {
        const response = await fetch('films.json');
        const data = await response.json();
        
        renderCurrentFilm(data.currentFilm);
        renderPastFilms(data.pastFilms);
    } catch (error) {
        console.error('Fehler beim Laden der Filmdaten:', error);
    }
}

function renderCurrentFilm(film) {
    const container = document.getElementById('current-film-container');
    container.innerHTML = createFilmCard(film, true);
}

function renderPastFilms(films) {
    const container = document.getElementById('past-films-container');
    container.innerHTML = films.map(film => createFilmCard(film, false)).join('');
}

function createFilmCard(film, isCurrent) {
    const dateLabel = isCurrent ? 'Anstehend am' : 'Gesehen am';
    
    return `
        <div class="film-card">
            <div class="film-header">
                <span class="film-title">${film.title}</span>
                <span class="film-year">${film.year}</span>
            </div>
            <div class="club-date">${dateLabel}: ${formatDate(film.clubDate)}</div>
            <div class="ratings">
                ${createRatingItem('derschaki', film.derschaki)}
                ${createRatingItem('zebrastuhl', film.zebrastuhl)}
            </div>
        </div>
    `;
}

function createRatingItem(name, ratingData) {
    const { rating, letterboxdUrl } = ratingData;
    
    if (!rating) {
        return `
            <div class="rating-item">
                <div class="rating-name">${name}</div>
                <div class="pending">Noch nicht bewertet</div>
            </div>
        `;
    }
    
    return `
        <div class="rating-item">
            <div class="rating-name">${name}</div>
            <div class="stars">${createStars(rating)}</div>
            ${letterboxdUrl ? `<a href="${letterboxdUrl}" target="_blank" class="letterboxd-link">→ Letterboxd</a>` : ''}
        </div>
    `;
}

function createStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    const emptyStars = 5 - Math.ceil(rating);
    
    let stars = '';
    
    for (let i = 0; i < fullStars; i++) {
        stars += '<span class="star filled">★</span>';
    }
    
    if (hasHalfStar) {
        stars += '<span class="star half">★</span>';
    }
    
    for (let i = 0; i < emptyStars; i++) {
        stars += '<span class="star">★</span>';
    }
    
    return stars;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('de-DE', { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric' 
    });
}

// Lade Filme beim Seitenaufruf
loadFilms();

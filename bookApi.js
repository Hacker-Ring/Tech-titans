// bookApi.js
// Fetch books from Open Library and Google Books APIs

async function fetchOpenLibraryBooks(query) {
    const response = await fetch(`https://openlibrary.org/search.json?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    return data.docs.slice(0, 5).map(book => ({
        title: book.title,
        author: book.author_name ? book.author_name.join(', ') : 'Unknown',
        source: 'Open Library',
        image: book.cover_i
            ? `https://covers.openlibrary.org/b/id/${book.cover_i}-M.jpg`
            : 'https://via.placeholder.com/128x192?text=No+Cover'
    }));
}

async function fetchGoogleBooks(query) {
    const response = await fetch(`https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    if (!data.items) return [];
    return data.items.slice(0, 5).map(item => ({
        title: item.volumeInfo.title,
        author: item.volumeInfo.authors ? item.volumeInfo.authors.join(', ') : 'Unknown',
        source: 'Google Books',
        image: item.volumeInfo.imageLinks && item.volumeInfo.imageLinks.thumbnail
            ? item.volumeInfo.imageLinks.thumbnail.replace('http:', 'https:')
            : 'https://via.placeholder.com/128x192?text=No+Cover'
    }));
}

export async function searchBooks(query) {
    const [openLibrary, googleBooks] = await Promise.all([
        fetchOpenLibraryBooks(query),
        fetchGoogleBooks(query)
    ]);
    return [...openLibrary, ...googleBooks];
}

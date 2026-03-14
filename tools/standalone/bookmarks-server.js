// server.js
// BOOKMARKS ORGANIZER API v1.0 – JSON-file backed REST API (Node + Express)
//npm init -y
//npm install express cors
//node bookmarks-server.js

const fs = require('fs');
const path = require('path');
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 4000;

// Path to JSON file
const DATA_FILE = path.join(__dirname, 'worklog-bookmarks.json');

// Middleware
app.use(cors());                // Allow all origins for local dev [web:63]
app.use(express.json());        // Parse JSON bodies [web:58]

// Helper: load bookmarks from file
function loadBookmarks() {
    try {
        if (!fs.existsSync(DATA_FILE)) {
            fs.writeFileSync(
                DATA_FILE,
                JSON.stringify({ bookmarks: [] }, null, 2),
                'utf8'
            ); // [web:62][web:65]
            return [];
        }
        const raw = fs.readFileSync(DATA_FILE, 'utf8'); // sync for simplicity [web:62][web:65]
        if (!raw.trim()) return [];
        const parsed = JSON.parse(raw);
        return Array.isArray(parsed) ? parsed : parsed.bookmarks || [];
    } catch (err) {
        console.error('Error reading data file:', err);
        return [];
    }
}

// Helper: save bookmarks to file
function saveBookmarks(bookmarks) {
    const payload = { bookmarks };
    fs.writeFileSync(DATA_FILE, JSON.stringify(payload, null, 2), 'utf8'); // [web:62][web:65]
}

// GET all bookmarks
app.get('/api/bookmarks', (req, res) => {
    const bookmarks = loadBookmarks();
    res.json({ data: bookmarks });
});

// GET single bookmark
app.get('/api/bookmarks/:id', (req, res) => {
    const bookmarks = loadBookmarks();
    const item = bookmarks.find((b) => b.id === req.params.id);
    if (!item) return res.status(404).json({ error: 'Bookmark not found' });
    res.json({ data: item });
});

// POST create bookmark
app.post('/api/bookmarks', (req, res) => {
    const bookmarks = loadBookmarks();
    const payload = req.body || {};

    if (!payload.url) {
        return res.status(400).json({ error: 'url is required' });
    }

    const nowIso = new Date().toISOString();
    const id = payload.id || String(Date.now());

    const domain = (() => {
        try {
            const u = new URL(payload.url);
            return u.hostname.replace(/^www\./, '');
        } catch {
            return '';
        }
    })();

    const newBookmark = {
        id,
        url: payload.url,
        title: payload.title || payload.url,
        description: payload.description || '',
        tags: payload.tags || [],
        collections: payload.collections || [],
        type: payload.type || 'article',
        createdAt: nowIso,
        updatedAt: nowIso,
        status: payload.status || 'to_read',
        rating: payload.rating || 0,
        favorite: !!payload.favorite,
        source: payload.source || 'manual',
        preview: payload.preview || { domain },
        lastVisitedAt: payload.lastVisitedAt || null,
        visitCount: payload.visitCount || 0,
        isDead: !!payload.isDead,
    };

    bookmarks.push(newBookmark);
    saveBookmarks(bookmarks);

    res.status(201).json({ data: newBookmark });
});

// PUT update bookmark
app.put('/api/bookmarks/:id', (req, res) => {
    const bookmarks = loadBookmarks();
    const index = bookmarks.findIndex((b) => b.id === req.params.id);
    if (index === -1) return res.status(404).json({ error: 'Bookmark not found' });

    const existing = bookmarks[index];
    const payload = req.body || {};
    const nowIso = new Date().toISOString();

    const updated = {
        ...existing,
        ...payload,
        id: existing.id,
        updatedAt: nowIso,
    };

    bookmarks[index] = updated;
    saveBookmarks(bookmarks);

    res.json({ data: updated });
});

// DELETE bookmark
app.delete('/api/bookmarks/:id', (req, res) => {
    const bookmarks = loadBookmarks();
    const next = bookmarks.filter((b) => b.id !== req.params.id);
    if (next.length === bookmarks.length) {
        return res.status(404).json({ error: 'Bookmark not found' });
    }
    saveBookmarks(next);
    res.status(204).send();
});

// Start server
app.listen(PORT, () => {
    console.log(`Bookmarks API listening on http://localhost:${PORT}`);
});

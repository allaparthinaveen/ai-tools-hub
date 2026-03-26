// API endpoint
const API_URL = '/api/ideas';

// Global variables
let allIdeas = [];
let currentFilter = 'all';
let currentSearchTerm = '';

// DOM elements
const ideasGrid = document.getElementById('ideasGrid');
const filterBtns = document.querySelectorAll('.filter-btn');
const searchInput = document.getElementById('searchInput');
const clearSearchBtn = document.getElementById('clearSearch');
const ideaCountSpan = document.getElementById('ideaCount');
const modal = document.getElementById('ideaModal');
const modalTitle = document.getElementById('modalTitle');
const modalCategory = document.getElementById('modalCategory');
const modalTags = document.getElementById('modalTags');
const modalDescription = document.getElementById('modalDescription');
const modalDifficulty = document.getElementById('modalDifficulty');
const modalTimeframe = document.getElementById('modalTimeframe');

// Fetch ideas from API
async function fetchIdeas() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error('Failed to fetch ideas');
        allIdeas = await response.json();
        renderIdeas();
        updateStats();
    } catch (error) {
        console.error('Error fetching ideas:', error);
        ideasGrid.innerHTML = '<div class="loading-spinner"><p style="color: #dc3545;">Failed to load ideas. Please check if the server is running.</p></div>';
    }
}

// Filter and search ideas
function getFilteredIdeas() {
    let filtered = [...allIdeas];

    // Apply category filter
    if (currentFilter !== 'all') {
        filtered = filtered.filter(idea => idea.category === currentFilter);
    }

    // Apply search filter
    if (currentSearchTerm) {
        const searchLower = currentSearchTerm.toLowerCase();
        filtered = filtered.filter(idea =>
            idea.title.toLowerCase().includes(searchLower) ||
            idea.shortDescription.toLowerCase().includes(searchLower) ||
            idea.longDescription.toLowerCase().includes(searchLower) ||
            idea.tags.some(tag => tag.toLowerCase().includes(searchLower))
        );
    }

    return filtered;
}

// Render ideas in bento grid
function renderIdeas() {
    const filteredIdeas = getFilteredIdeas();

    if (filteredIdeas.length === 0) {
        ideasGrid.innerHTML = `
            <div class="loading-spinner" style="grid-column: 1/-1;">
                <p style="font-size: 1.1rem;">✨ No ideas found</p>
                <p style="color: #6c757d; font-size: 0.9rem;">Try adjusting your search or filter</p>
            </div>
        `;
        return;
    }

    ideasGrid.innerHTML = filteredIdeas.map(idea => `
        <article class="card" data-id="${idea.id}" data-category="${idea.category}">
            <div class="card-icon">${idea.imagePlaceholder || '💡'}</div>
            <div class="category-tag" data-category="${idea.category}">${idea.category}</div>
            <h3 class="card-title">${escapeHtml(idea.title)}</h3>
            <p class="card-description">${escapeHtml(idea.shortDescription)}</p>
        </article>
    `).join('');

    // Add click listeners to cards
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', () => openModal(parseInt(card.dataset.id)));
    });
}

// Open modal with idea details
function openModal(ideaId) {
    const idea = allIdeas.find(i => i.id === ideaId);
    if (!idea) return;

    modalTitle.textContent = idea.title;
    modalCategory.textContent = idea.category;
    modalCategory.className = `modal-category category-tag`;
    modalCategory.setAttribute('data-category', idea.category);

    modalTags.innerHTML = idea.tags.map(tag => `<span>${escapeHtml(tag)}</span>`).join('');
    modalDescription.textContent = idea.longDescription;
    modalDifficulty.textContent = idea.difficulty;
    modalTimeframe.textContent = idea.timeframe;

    modal.classList.add('show');
}

// Close modal
function closeModal() {
    modal.classList.remove('show');
}

// Update stats display
function updateStats() {
    const filteredCount = getFilteredIdeas().length;
    ideaCountSpan.textContent = `${filteredCount} ${filteredCount === 1 ? 'idea' : 'ideas'}`;
}

// Handle filter change
function setFilter(category) {
    currentFilter = category;

    // Update active button styling
    filterBtns.forEach(btn => {
        if (btn.dataset.category === category) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    renderIdeas();
    updateStats();
}

// Handle search
function handleSearch() {
    currentSearchTerm = searchInput.value.trim();
    clearSearchBtn.style.display = currentSearchTerm ? 'block' : 'none';
    renderIdeas();
    updateStats();
}

// Clear search
function clearSearch() {
    searchInput.value = '';
    currentSearchTerm = '';
    clearSearchBtn.style.display = 'none';
    renderIdeas();
    updateStats();
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Event Listeners
filterBtns.forEach(btn => {
    btn.addEventListener('click', () => setFilter(btn.dataset.category));
});

searchInput.addEventListener('input', handleSearch);
clearSearchBtn.addEventListener('click', clearSearch);

// Modal close handlers
modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
});

document.querySelector('.modal-close').addEventListener('click', closeModal);

// Close modal with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('show')) {
        closeModal();
    }
});

// ── Theme Toggle ──────────────────────────────────────────────
const themeToggleBtn = document.getElementById('themeToggleBtn');
const themeIcon = themeToggleBtn.querySelector('.theme-icon');

function applyTheme(theme) {
    if (theme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        themeIcon.textContent = '☀️';
    } else {
        document.documentElement.removeAttribute('data-theme');
        themeIcon.textContent = '🌙';
    }
    localStorage.setItem('ideaRepoTheme', theme);
}

// Load saved preference (default: dark)
applyTheme(localStorage.getItem('ideaRepoTheme') || 'dark');

themeToggleBtn.addEventListener('click', () => {
    const isLight = document.documentElement.getAttribute('data-theme') === 'light';
    applyTheme(isLight ? 'dark' : 'light');
});

// Initialize app
fetchIdeas();
const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());
app.use(express.static('public'));

// API endpoint to get ideas
app.get('/api/ideas', (req, res) => {
    try {
        const ideasData = fs.readFileSync(path.join(__dirname, 'ideas.json'), 'utf8');
        const ideas = JSON.parse(ideasData);
        res.json(ideas);
    } catch (error) {
        console.error('Error reading ideas.json:', error);
        res.status(500).json({ error: 'Failed to load ideas' });
    }
});

// Optional: POST endpoint to add new ideas
app.post('/api/ideas', (req, res) => {
    try {
        const newIdea = req.body;
        const ideasData = fs.readFileSync(path.join(__dirname, 'ideas.json'), 'utf8');
        const ideas = JSON.parse(ideasData);

        newIdea.id = Date.now(); // Simple ID generation
        ideas.push(newIdea);

        fs.writeFileSync(path.join(__dirname, 'ideas.json'), JSON.stringify(ideas, null, 2));
        res.status(201).json(newIdea);
    } catch (error) {
        console.error('Error saving idea:', error);
        res.status(500).json({ error: 'Failed to save idea' });
    }
});

app.listen(PORT, () => {
    console.log(`🚀 Server running at http://localhost:${PORT}`);
});
const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = path.join(__dirname, 'progress.json');

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Initialize progress file if it doesn't exist
function getProgress() {
    try {
        if (fs.existsSync(DATA_FILE)) {
            return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
        }
    } catch (e) {
        console.error('Error reading progress:', e);
    }
    return {};
}

function saveProgress(data) {
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf8');
}

// GET /api/progress - Fetch all progress
app.get('/api/progress', (req, res) => {
    res.json(getProgress());
});

// POST /api/progress - Update a single checkbox
// Body: { problemId: "138", user: "dilshad", solved: true }
app.post('/api/progress', (req, res) => {
    const { problemId, user, solved } = req.body;
    if (!problemId || !user) {
        return res.status(400).json({ error: 'Missing problemId or user' });
    }

    const progress = getProgress();
    if (!progress[problemId]) {
        progress[problemId] = {};
    }
    progress[problemId][user] = solved;
    saveProgress(progress);

    res.json({ success: true, progress });
});

// GET /api/stats - Get summary statistics
app.get('/api/stats', (req, res) => {
    const progress = getProgress();
    const stats = { dilshad: 0, yash: 0 };

    for (const pid in progress) {
        if (progress[pid].dilshad) stats.dilshad++;
        if (progress[pid].yash) stats.yash++;
    }

    res.json(stats);
});

app.listen(PORT, () => {
    console.log(`\n🚀 Interview Prep Tracker running at http://localhost:${PORT}`);
    console.log(`   Share this URL on your network for Yash to access.\n`);
});

# app/toolkit_data.py

TOOLKIT_CONTENT = {
    "stressed": {
        "videos": [
            { "id": 1, "title": "Quick Calm", "url": "https://www.youtube.com/embed/inpok4MKVLM", "color": "from-blue-400 to-cyan-500", "sub": "Stress Relief" },
            { "id": 2, "title": "5 Min Mindfulness", "url": "https://www.youtube.com/embed/ZToicY62f1U", "color": "from-yellow-400 to-orange-500", "sub": "Quick Boost" }
        ],
        "activities": [
            { "id": 8, "title": "Zen Doodle Pad", "actId": "doodle", "color": "from-pink-400 to-rose-500", "sub": "Draw your stress away" }
        ],
        "stories": {
            "romance": [], "comedy": [], "suspense": [], 
            "wisdom": [{ "id": 401, "title": "The Silent Forest", "content": "Silence is a song...", "sub": "Zen • 5 min", "color": "from-teal-400 to-green-500" }]
        }
    },
    "neutral": {
        "videos": [
            { "id": 3, "title": "Deep Focus Lo-Fi", "url": "https://www.youtube.com/embed/jfKfPfyJRdk", "color": "from-indigo-400 to-purple-500", "sub": "Study/Work" }
        ],
        "activities": [],
        "stories": { "romance": [], "comedy": [], "suspense": [], "wisdom": [] }
    },

    "happy": {
    "videos": [
        { "id": 5, "title": "Keep the Vibe High", "url": "https://www.youtube.com/embed/ZbZSe6N_BXs", "color": "from-yellow-400 to-orange-500", "sub": "Stay Positive" }
    ],
    "activities": [
        { "id": 15, "title": "Gratitude List", "actId": "journal", "color": "from-teal-400 to-emerald-500", "sub": "Write 3 good things" }
    ],
    "stories": {
        "romance": [], "comedy": [], "suspense": [], "wisdom": []
    }
    }
}
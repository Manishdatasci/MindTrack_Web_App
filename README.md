# MindTrack – Personal Wellness & Habit Tracker

MindTrack helps you track daily habits, moods, and progress. It uses a **Streamlit frontend** that communicates with a **FastAPI backend**. Data is stored locally in CSV format.

## Features
- Daily habit check-in (Water, Exercise, Meditation, Reading, Journaling)
- Mood tracking (Happy, Neutral, Sad)
- Habit completion analytics (bar chart, line chart)
- Calendar heatmap for streaks
- AI-based habit suggestions
- Download progress as CSV
- Motivational messages

## Project Structure
MindTrack/
├── main.py           # Streamlit frontend  
├── app.py            # FastAPI backend  
├── data/             # CSV storage  
│   └── user_data.csv  
├── requirements.txt  
└── README.md  


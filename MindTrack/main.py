import streamlit as st
import pandas as pd
import datetime
import random
import requests
import matplotlib.pyplot as plt
import calplot

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"

# Helper Functions
def get_data():
    """Fetch data from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/get_data")
        if response.status_code == 200:
            return pd.DataFrame(response.json())
    except:
        st.error("❌ Could not connect to backend!")
    return pd.DataFrame(columns=["date", "habit", "completed", "mood"])

def save_progress(entries):
    """Send multiple habits to backend"""
    try:
        response = requests.post(f"{BACKEND_URL}/save_progress_bulk", json=entries)
        if response.status_code == 200:
            st.success("✅ Today's progress saved successfully!")
        else:
            st.error("❌ Failed to save progress!")
    except:
        st.error("❌ Could not connect to backend!")

def get_motivation():
    messages = [
        "Keep going! Small steps lead to big changes 💪",
        "You’re doing amazing — stay consistent 🌟",
        "Remember why you started ❤️",
        "Progress, not perfection 🙌",
        "Stay hydrated and positive 💧😊",
        "Your future self will thank you 🌈"
    ]
    return random.choice(messages)

def suggest_habits(df):
    if df.empty:
        return "Start tracking to get habit suggestions!"
    habit_avg = df.groupby('habit')['completed'].mean()
    weak_habits = habit_avg[habit_avg < 0.6].index.tolist()
    if weak_habits:
        return f"Try focusing on: {', '.join(weak_habits)} next week 💪"
    else:
        return "Great consistency! Maybe add a new habit like Stretching or Gratitude 🌟"

# Page Layout
st.set_page_config(page_title="MindTrack", page_icon="🧠", layout="wide")
st.title("🧠 MindTrack – Personal Wellness & Habit Tracker")
st.caption("Track your habits, moods, and progress every day 💖")

# Daily Habit Input
today = datetime.date.today()
st.subheader("✅ Daily Habit Check-In")
col1, col2 = st.columns(2)
with col1:
    selected_mood = st.radio("How are you feeling today?", ["😊 Happy", "😐 Neutral", "😔 Sad"])
with col2:
    st.write("### Today's Date:")
    st.info(today.strftime("%A, %d %B %Y"))

habits = ["Water Intake", "Exercise", "Meditation", "Reading", "Journaling"]
completed_habits = [habit for habit in habits if st.checkbox(habit)]

if st.button("💾 Save Today's Progress"):
    entries = []
    for habit in habits:
        entries.append({
            "date": str(today),
            "habit": habit,
            "completed": habit in completed_habits,
            "mood": selected_mood
        })
    save_progress(entries)  

# Analytics Section
st.markdown("---")
st.subheader("📈 Your Progress Analytics")

df = get_data()
if not df.empty:
    df["date"] = pd.to_datetime(df["date"])

    # Habit Completion Rate
    st.write("### 💪 Habit Completion Rate (%)")
    habit_summary = df.groupby("habit")["completed"].mean() * 100
    st.bar_chart(habit_summary)

    # Daily Progress
    st.write("### 📅 Daily Completion Trend")
    daily_progress = df.groupby("date")["completed"].mean() * 100
    st.line_chart(daily_progress)

    # Mood Tracker
    st.write("### 💭 Mood Tracker")
    mood_trend = df.groupby("date")["mood"].last().reset_index()
    st.dataframe(mood_trend)

    # Calendar Heatmap
    st.write("### 🗓️ Streak Calendar")
    daily_counts = df.groupby("date")["completed"].mean()
    if not daily_counts.empty:
        fig, ax = calplot.calplot(daily_counts)
        st.pyplot(fig)

    # Download CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Your Progress", data=csv, file_name="mindtrack_progress.csv", mime="text/csv")

else:
    st.info("No data yet! Start tracking your habits today.")

# AI Habit Suggestion
st.markdown("---")
st.subheader("🤖 Habit Suggestions")
st.success(suggest_habits(df))

# Daily Motivation
st.markdown("---")
st.subheader("💬 Daily Motivation")
st.success(get_motivation())

# Branding
st.markdown("---")
st.markdown("<p style='text-align: center;'>Developed with ❤️ by <b>Manish Kumar Rajak</b></p>", unsafe_allow_html=True)




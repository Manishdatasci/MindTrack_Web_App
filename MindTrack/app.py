
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import os

app = FastAPI(title="MindTrack Backend API")

DATA_PATH = "data/user_data.csv"
os.makedirs("data", exist_ok=True)

class HabitEntry(BaseModel):
    date: str
    habit: str
    completed: bool
    mood: str

@app.get("/get_data")
def get_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        df = pd.DataFrame(columns=["date", "habit", "completed", "mood"])
    return df.to_dict(orient="records")

@app.post("/save_progress_bulk")
def save_progress_bulk(entries: List[HabitEntry]):
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        df = pd.DataFrame(columns=["date", "habit", "completed", "mood"])
    new_entries = pd.DataFrame([entry.dict() for entry in entries])
    df = pd.concat([df, new_entries], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    return {"message": "Progress saved successfully!"}

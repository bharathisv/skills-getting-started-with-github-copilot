"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Tennis Club": {
        "description": "Learn tennis techniques and participate in friendly matches",
        "schedule": "Saturdays, 9:00 AM - 10:30 AM",
        "max_participants": 16,
        "participants": ["alex@mergington.edu", "sophie@mergington.edu", "marcus@mergington.edu"]
        },
        "Basketball Team": {
        "description": "Competitive basketball team for intramural and regional tournaments",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu", "lucas@mergington.edu", "tyler@mergington.edu", "aisha@mergington.edu", "carlos@mergington.edu"]
        },
        "Art Club":  {
        "description": "Explore various art mediums including painting, drawing, and sculpture",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "maya@mergington.edu", "jacob@mergington.edu", "zoe@mergington.edu"]
        },
        "Music Ensemble": {
        "description": "Practice and perform classical and contemporary music together",
        "schedule": "Tuesdays and Thursdays, 4:30 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu", "ava@mergington.edu", "liam@mergington.edu", "olivia@mergington.edu", "ethan@mergington.edu"]
        },
        "Robotics Club": {
        "description": "Design, build, and program robots for competitions",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["ethan@mergington.edu", "priya@mergington.edu", "kobe@mergington.edu", "nina@mergington.edu", "alex@mergington.edu"]
        },
        "Debate Team": {
        "description": "Develop argumentation and public speaking skills through competitive debate",
        "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 12,
        "participants": ["grace@mergington.edu", "mason@mergington.edu", "jordan@mergington.edu", "riley@mergington.edu"]
        },
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu", "sarah@mergington.edu", "james@mergington.edu", "victor@mergington.edu", "emma@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu", "ryan@mergington.edu", "alex@mergington.edu", "jade@mergington.edu", "kevin@mergington.edu", "natalie@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu", "marcus@mergington.edu", "aisha@mergington.edu", "tyler@mergington.edu", "brittany@mergington.edu", "david@mergington.edu", "sophie@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    
    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}

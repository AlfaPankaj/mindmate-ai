import asyncio
import motor.motor_asyncio
import os
import certifi
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, ".env")

load_dotenv(dotenv_path=env_path)

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/mindmate")
USER_ID = "demo_user_001"

async def seed():
    uri = MONGODB_URI
    print(f"Connecting to MongoDB Atlas cluster...")
    client = motor.motor_asyncio.AsyncIOMotorClient(
        uri, 
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True
    )
    db = client.get_database("mindmate")
    
    await db.user_profiles.delete_many({"user_id": USER_ID})
    await db.moods.delete_many({"user_id": USER_ID})
    await db.habits.delete_many({"user_id": USER_ID})
    await db.journals.delete_many({"user_id": USER_ID})
    
    profile = {
        "user_id": USER_ID,
        "active_concerns": ["sleep difficulties", "work stress"],
        "active_patterns": {
            "sleep_difficulty": {
                "pattern_type": "sleep_difficulty",
                "evidence_count": 3,
                "first_seen": datetime.now(timezone.utc) - timedelta(days=14),
                "last_seen": datetime.now(timezone.utc) - timedelta(days=2)
            }
        },
        "preferences": {
            "intervention_style": "supportive",
            "checkin_time": "20:00",
            "checkin_enabled": True
        },
        "last_updated": datetime.now(timezone.utc)
    }
    await db.user_profiles.insert_one(profile)
    
    habit = {
        "user_id": USER_ID,
        "name": "Evening Meditation",
        "status": "abandoned",
        "streak": 0,
        "last_completed": datetime.now(timezone.utc) - timedelta(days=5),
        "created_at": datetime.now(timezone.utc) - timedelta(days=10)
    }
    await db.habits.insert_one(habit)
    
    moods = [
        {"user_id": USER_ID, "score": 4, "timestamp": datetime.now(timezone.utc) - timedelta(days=3)},
        {"user_id": USER_ID, "score": 3, "timestamp": datetime.now(timezone.utc) - timedelta(days=2)},
        {"user_id": USER_ID, "score": 2, "timestamp": datetime.now(timezone.utc) - timedelta(days=1)},
    ]
    await db.moods.insert_many(moods)
    
    print("Database seeded with 'Sleep Pattern' demo data!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed())

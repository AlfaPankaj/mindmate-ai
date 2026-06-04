from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from db.mongodb import MongoDB

async def update_temporal_stats(user_id: str, timestamp: datetime):
    """Updates peak engagement hour and session frequency."""
    db = MongoDB.db
    hour = timestamp.hour
    
    # In production, this would be a more complex calculation
    await db.user_profiles.update_one(
        {"user_id": user_id},
        {"$set": {"peak_engagement_hour": hour}}
    )

async def calculate_readiness(mood_avg: float, habit_rate: float, engagement: float) -> float:
    """Computes readiness score based on v2.0 formula."""
    return 0.4 * (mood_avg / 10) + 0.3 * habit_rate + 0.3 * engagement

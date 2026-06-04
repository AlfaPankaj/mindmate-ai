from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from db.mongodb import MongoDB

class UserPattern(BaseModel):
    pattern_type: str
    evidence_count: int = 1
    first_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = {}

class OutcomeEntry(BaseModel):
    score: int = 0  
    last_used: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    use_count: int = 1

class UserProfile(BaseModel):
    user_id: str
    communication_style: str = "direct"
    emotional_vocabulary_level: str = "high"
    active_concerns: List[str] = []
    active_patterns: Dict[str, UserPattern] = {}
    outcome_history: Dict[str, OutcomeEntry] = {}

    # v2.0 Additions: Temporal & Emotional Trajectory
    peak_engagement_hour: Optional[int] = None
    session_frequency_days: float = 0.0
    longest_streak: int = 0
    mood_trend_7d: str = "stable"  # improving, stable, declining
    last_positive_session: Optional[datetime] = None

    # Intervention History
    interventions_offered: List[Dict[str, Any]] = []
    ignored_nudges: List[str] = []

    # Cross-module correlations
    sleep_mood_correlation: float = 0.0
    habit_dropout_day: Optional[int] = None

    privacy_settings: Dict[str, Any] = {
        "allow_historical_patterns": True,
        "consent_depth": "recent"
    }
    preferences: Dict[str, Any] = {
        "intervention_style": "supportive",
        "checkin_time": "20:00",
        "checkin_enabled": True
    }
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


async def get_prism_profile(user_id: str) -> Optional[UserProfile]:
    """Fetches the PRISM-Lite profile for a user."""
    db = MongoDB.db
    profile_data = await db.user_profiles.find_one({"user_id": user_id})
    if profile_data:
        return UserProfile(**profile_data)
    return None

async def create_initial_profile(user_id: str) -> UserProfile:
    """Creates a new PRISM-Lite profile for a new user (Cold Start)."""
    db = MongoDB.db
    new_profile = UserProfile(user_id=user_id)
    await db.user_profiles.insert_one(new_profile.model_dump())
    return new_profile

async def update_pattern(user_id: str, pattern_type: str, metadata: Dict[str, Any] = None):
    """Updates or adds a detected behavioral pattern."""
    db = MongoDB.db
    now = datetime.now(timezone.utc)
    
    update_query = {
        f"active_patterns.{pattern_type}.evidence_count": 1,
        "last_updated": now
    }
    
    set_query = {
        f"active_patterns.{pattern_type}.last_seen": now,
        f"active_patterns.{pattern_type}.pattern_type": pattern_type
    }
    
    if metadata:
        set_query[f"active_patterns.{pattern_type}.metadata"] = metadata

    await db.user_profiles.update_one(
        {"user_id": user_id},
        {"$inc": {f"active_patterns.{pattern_type}.evidence_count": 1}, "$set": set_query},
        upsert=True
    )

async def log_outcome(user_id: str, action_type: str, score: int):
    """Tracks if a recommendation helped the user."""
    db = MongoDB.db
    now = datetime.now(timezone.utc)
    
    await db.user_profiles.update_one(
        {"user_id": user_id},
        {
            "$inc": {f"outcome_history.{action_type}.use_count": 1},
            "$set": {
                f"outcome_history.{action_type}.score": score,
                f"outcome_history.{action_type}.last_used": now,
                "last_updated": now
            }
        },
        upsert=True
    )

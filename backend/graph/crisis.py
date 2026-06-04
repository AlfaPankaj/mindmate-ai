import re
from typing import Dict, Any, Optional

# N0: Crisis Pre-filter
# Regex scan for 12 hard crisis phrases. Zero LLM involvement. Guaranteed delivery.
CRISIS_PHRASES = [
    r"\bwant to die\b",
    r"\bend my life\b",
    r"\bkill myself\b",
    r"\bno reason to live\b",
    r"\bsuicidal\b",
    r"\bself-harm\b",
    r"\bbetter off dead\b",
    r"\bend it all\b",
    r"\bsleep forever\b", # euphemism
    r"\bhurt myself\b",
    r"\bcan't go on\b",
    r"\bjumping off\b"
]

CRISIS_RESPONSE = """
I hear how much pain you're in, and I'm very concerned about your safety. Please reach out to someone who can help right now.

You can contact:
- iCall (Psychosocial Helpline): 9152987821
- Vandrevala Foundation: 9999666555
- Local Emergency Services: 112

I am an AI, and while I'm here to support you, these professionals can provide the immediate assistance you need. You don't have to go through this alone.
"""

def crisis_pre_filter(message: str) -> Optional[str]:
    for phrase in CRISIS_PHRASES:
        if re.search(phrase, message.lower()):
            return CRISIS_RESPONSE
    return None

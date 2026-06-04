from typing import Annotated, List, Dict, Any, TypedDict
from operator import add

class CompanionState(TypedDict):
    user_id: str
    message: str      
    # PRISM-Lite profile data      
    profile: Dict[str, Any] 
    module_data: Dict[str, Any] 
    intent_category: str    
    detected_patterns: Annotated[List[str], add] 
    recommendation: Dict[str, Any] 
    response: str           
    risk_level: str         
    safety_flag: bool      
    is_proactive: bool      

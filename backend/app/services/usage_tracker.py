"""
Simple usage statistics tracker for admin reporting.
Stores session data in a JSON file for easy export.
"""
import json
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Path to store usage data
USAGE_FILE = Path(__file__).parent.parent.parent / "usage_stats.json"


def load_usage_data() -> List[Dict[str, Any]]:
    """Load existing usage data from file."""
    if not USAGE_FILE.exists():
        return []
    
    try:
        with open(USAGE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading usage data: {e}")
        return []


def save_usage_data(data: List[Dict[str, Any]]):
    """Save usage data to file."""
    try:
        with open(USAGE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving usage data: {e}")


def track_session_start(user_id: str, timestamp: Optional[str] = None):
    """Track when a new session starts."""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    data = load_usage_data()
    
    # Check if session already exists
    for session in data:
        if session.get('user_id') == user_id:
            return  # Session already tracked
    
    data.append({
        'user_id': user_id,
        'session_start': timestamp,
        'age': None,
        'location': None,
        'gender': None,
        'cancer_type': None,
        'cancer_stage': None,
        'comorbidities': [],
        'prior_treatments': [],
        'messages_sent': 0,
        'trials_found': 0,
        'session_end': None,
        'total_duration_seconds': None
    })
    
    save_usage_data(data)
    logger.info(f"Started tracking session for user {user_id}")


def track_intake_form(
    user_id: str,
    age: int,
    location: str,
    gender: str,
    cancer_type: str,
    cancer_stage: str,
    comorbidities: List[str],
    prior_treatments: List[str]
):
    """Track intake form submission with user demographics."""
    data = load_usage_data()
    
    # Find or create session
    session = None
    for s in data:
        if s.get('user_id') == user_id:
            session = s
            break
    
    if session is None:
        track_session_start(user_id)
        data = load_usage_data()
        session = data[-1]
    
    # Update session with intake data
    session['age'] = age
    session['location'] = location
    session['gender'] = gender
    session['cancer_type'] = cancer_type
    session['cancer_stage'] = cancer_stage
    session['comorbidities'] = comorbidities
    session['prior_treatments'] = prior_treatments
    
    save_usage_data(data)
    logger.info(f"Tracked intake form for user {user_id}")


def track_message(user_id: str):
    """Track a message sent by user."""
    data = load_usage_data()
    
    for session in data:
        if session.get('user_id') == user_id:
            session['messages_sent'] = session.get('messages_sent', 0) + 1
            save_usage_data(data)
            return
    
    # If session doesn't exist, create it
    track_session_start(user_id)
    track_message(user_id)


def track_trials_found(user_id: str, count: int):
    """Track number of trials found for user."""
    data = load_usage_data()
    
    for session in data:
        if session.get('user_id') == user_id:
            session['trials_found'] = count
            save_usage_data(data)
            return


def track_session_end(user_id: str):
    """Track when a session ends."""
    data = load_usage_data()
    
    for session in data:
        if session.get('user_id') == user_id and session.get('session_end') is None:
            session['session_end'] = datetime.now().isoformat()
            
            # Calculate duration
            if session.get('session_start'):
                try:
                    start = datetime.fromisoformat(session['session_start'])
                    end = datetime.fromisoformat(session['session_end'])
                    duration = (end - start).total_seconds()
                    session['total_duration_seconds'] = duration
                except Exception as e:
                    logger.error(f"Error calculating duration: {e}")
            
            save_usage_data(data)
            logger.info(f"Ended session for user {user_id}")
            return


def get_all_usage_data() -> List[Dict[str, Any]]:
    """Get all usage data for export."""
    return load_usage_data()


def clear_usage_data():
    """Clear all usage data (for testing or after export)."""
    save_usage_data([])
    logger.info("Cleared all usage data")

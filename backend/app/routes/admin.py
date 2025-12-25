"""
Admin routes for usage statistics and monitoring.
"""
from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
import csv
import io
from datetime import datetime
from app.services import usage_tracker
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/admin/stats")
async def get_stats_summary():
    """Get summary statistics for admin dashboard."""
    data = usage_tracker.get_all_usage_data()
    
    total_sessions = len(data)
    completed_sessions = len([s for s in data if s.get('session_end') is not None])
    
    # Cancer type breakdown
    cancer_types = {}
    for session in data:
        ct = session.get('cancer_type')
        if ct:
            cancer_types[ct] = cancer_types.get(ct, 0) + 1
    
    # Location breakdown
    locations = {}
    for session in data:
        loc = session.get('location')
        if loc:
            locations[loc] = locations.get(loc, 0) + 1
    
    # Age breakdown
    age_groups = {'<40': 0, '40-50': 0, '50-60': 0, '60-70': 0, '70+': 0}
    for session in data:
        age = session.get('age')
        if age:
            if age < 40:
                age_groups['<40'] += 1
            elif age < 50:
                age_groups['40-50'] += 1
            elif age < 60:
                age_groups['50-60'] += 1
            elif age < 70:
                age_groups['60-70'] += 1
            else:
                age_groups['70+'] += 1
    
    total_messages = sum(s.get('messages_sent', 0) for s in data)
    total_trials_found = sum(s.get('trials_found', 0) for s in data)
    
    return {
        "total_sessions": total_sessions,
        "completed_sessions": completed_sessions,
        "total_messages": total_messages,
        "total_trials_found": total_trials_found,
        "cancer_types": cancer_types,
        "locations": locations,
        "age_groups": age_groups,
        "last_updated": datetime.now().isoformat()
    }


@router.get("/admin/export-csv")
async def export_stats_csv():
    """
    Export usage statistics as CSV file for easy Google Sheets import.
    Admin can download this file and upload to Google Sheets.
    """
    data = usage_tracker.get_all_usage_data()
    
    # Create CSV in memory
    output = io.StringIO()
    
    if not data:
        # Return empty CSV with headers
        writer = csv.writer(output)
        writer.writerow([
            'User ID', 'Session Start', 'Session End', 'Duration (minutes)',
            'Age', 'Gender', 'Location', 'Cancer Type', 'Cancer Stage',
            'Comorbidities', 'Prior Treatments', 'Messages Sent', 'Trials Found'
        ])
    else:
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'User ID', 'Session Start', 'Session End', 'Duration (minutes)',
            'Age', 'Gender', 'Location', 'Cancer Type', 'Cancer Stage',
            'Comorbidities', 'Prior Treatments', 'Messages Sent', 'Trials Found'
        ])
        
        # Write data rows
        for session in data:
            # Format duration
            duration = session.get('total_duration_seconds')
            duration_minutes = round(duration / 60, 1) if duration else ''
            
            # Format timestamp
            session_start = session.get('session_start', '')
            if session_start:
                try:
                    dt = datetime.fromisoformat(session_start)
                    session_start = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass
            
            session_end = session.get('session_end', '')
            if session_end:
                try:
                    dt = datetime.fromisoformat(session_end)
                    session_end = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass
            
            # Format lists
            comorbidities = ', '.join(session.get('comorbidities', []))
            prior_treatments = ', '.join(session.get('prior_treatments', []))
            
            writer.writerow([
                session.get('user_id', ''),
                session_start,
                session_end,
                duration_minutes,
                session.get('age', ''),
                session.get('gender', ''),
                session.get('location', ''),
                session.get('cancer_type', ''),
                session.get('cancer_stage', ''),
                comorbidities,
                prior_treatments,
                session.get('messages_sent', 0),
                session.get('trials_found', 0)
            ])
    
    # Prepare response
    output.seek(0)
    
    # Generate filename with timestamp
    filename = f"chatbot_usage_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/admin/clear-stats")
async def clear_stats():
    """
    Clear all usage statistics.
    USE WITH CAUTION - this deletes all data!
    """
    usage_tracker.clear_usage_data()
    
    return {
        "status": "success",
        "message": "All usage statistics cleared",
        "timestamp": datetime.now().isoformat()
    }

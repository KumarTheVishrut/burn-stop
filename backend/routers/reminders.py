from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
import time

from models.service import Reminder, ReminderAcknowledge
from models.user import User
from routers.auth import get_current_user
from utils.redis_db import redis_db

router = APIRouter(tags=["reminders"])

@router.get("/organizations/{org_id}/reminders", response_model=List[Reminder])
async def get_upcoming_reminders(
    org_id: str,
    current_user: User = Depends(get_current_user)
):
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get current timestamp
    current_timestamp = int(time.time())
    
    # Get upcoming reminders (next 30 days)
    thirty_days_ahead = current_timestamp + (30 * 24 * 60 * 60)
    
    reminders_key = f"reminders:{org_id}"
    print(f"Debug: Checking reminders for org {org_id}")
    print(f"Debug: Current timestamp: {current_timestamp}")
    print(f"Debug: 30 days ahead: {thirty_days_ahead}")
    print(f"Debug: Reminders key: {reminders_key}")
    
    # Get reminders from current time to 30 days ahead using zrangebyscore
    upcoming_reminders = redis_db.zrangebyscore(
        reminders_key, 
        current_timestamp, 
        thirty_days_ahead, 
        withscores=True
    )
    
    print(f"Debug: Found {len(upcoming_reminders)} upcoming reminders: {upcoming_reminders}")
    
    reminders = []
    for service_id, score in upcoming_reminders:
        # Get service details
        service_key = f"service:{service_id}"
        service_data = redis_db.get(service_key)
        
        if service_data and service_data.get("status") == "active":
            reminder = Reminder(
                id=f"reminder_{service_id}_{int(score)}",
                service_id=service_id,
                service_name=service_data["name"],
                cost=service_data["cost"],
                reminder_date=datetime.fromtimestamp(score).isoformat(),
                org_id=org_id
            )
            reminders.append(reminder)
    
    # Sort by reminder date
    reminders.sort(key=lambda x: x.reminder_date)
    
    return reminders

@router.post("/reminders/{reminder_id}/acknowledge")
async def acknowledge_reminder(
    reminder_id: str,
    acknowledgment: ReminderAcknowledge,
    current_user: User = Depends(get_current_user)
):
    # Parse reminder_id to get service_id and timestamp
    try:
        parts = reminder_id.split("_")
        service_id = "_".join(parts[1:-1])  # Handle UUIDs with underscores
        timestamp = int(parts[-1])
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid reminder ID format")
    
    # Get service to verify access
    service_key = f"service:{service_id}"
    service_data = redis_db.get(service_key)
    
    if not service_data:
        raise HTTPException(status_code=404, detail="Service not found")
    
    org_id = service_data["org_id"]
    
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Store acknowledgment
    ack_key = f"acknowledgment:{reminder_id}"
    ack_data = {
        "reminder_id": reminder_id,
        "service_id": service_id,
        "user_id": current_user.id,
        "action_taken": acknowledgment.action_taken,
        "acknowledged_at": datetime.utcnow().isoformat()
    }
    redis_db.set(ack_key, ack_data)
    
    # Remove from active reminders
    reminders_key = f"reminders:{org_id}"
    redis_db.zrem(reminders_key, service_id)
    
    return {"message": "Reminder acknowledged successfully"}

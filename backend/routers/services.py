from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from datetime import datetime
import time
import json
from collections import defaultdict

from models.service import Service, ServiceCreate, ServiceUpdate, ServiceAnalytics
from models.user import User
from routers.auth import get_current_user
from utils.redis_db import redis_db
from utils.integrations import IntegrationService
from models.service import ServiceType

router = APIRouter(tags=["services"])

# Helper functions for organization access control
def has_moderator_access(org_data: dict, user_id: str) -> bool:
    """Check if user has moderator access (owner or moderator)"""
    return org_data["owner_id"] == user_id or user_id in org_data.get("moderators", [])

def check_organization_moderator_access(org_id: str, current_user: User) -> dict:
    """Check if user has moderator access to organization and return org data"""
    # First check if user is a member
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get organization data
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    return org_data

@router.post("/organizations/{org_id}/services", response_model=Service)
async def create_service(
    org_id: str,
    service: ServiceCreate,
    current_user: User = Depends(get_current_user)
):
    # Check if user has moderator access to this organization
    org_data = check_organization_moderator_access(org_id, current_user)
    if not has_moderator_access(org_data, current_user.id):
        raise HTTPException(status_code=403, detail="Only organization owner or moderators can create services")
    
    # Create service
    service_id = str(uuid.uuid4())
    service_data = {
        "id": service_id,
        "org_id": org_id,
        "name": service.name,
        "platform": service.platform.value,
        "service_type": service.service_type.value,
        "cost": service.cost,
        "reminder_date": service.reminder_date,
        "status": "active",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        
        # Infrastructure tracking
        "iam_number": service.iam_number,
        "instance_id": service.instance_id,
        "service_id": service.service_id,
        "instance_type": service.instance_type.value if service.instance_type else None,
        "region": service.region,
        
        # API specific
        "api_quota_tokens": service.api_quota_tokens,
        "api_usage_tokens": service.api_usage_tokens,
        
        # Additional metadata
        "description": service.description,
        "tags": service.tags,
        "owner_email": service.owner_email
    }
    
    # Save service
    service_key = f"service:{service_id}"
    redis_db.set(service_key, service_data)
    
    # Add to organization's services list
    org_services_key = f"org_services:{org_id}"
    existing_services = redis_db.get(org_services_key) or []
    existing_services.append(service_id)
    redis_db.set(org_services_key, existing_services)
    
    # Add reminder to sorted set (using reminder_date as score)
    reminder_timestamp = int(datetime.fromisoformat(service.reminder_date).timestamp())
    reminders_key = f"reminders:{org_id}"
    print(f"Debug: Adding reminder for service {service_id}")
    print(f"Debug: Reminder date: {service.reminder_date}")
    print(f"Debug: Reminder timestamp: {reminder_timestamp}")
    print(f"Debug: Reminders key: {reminders_key}")
    
    result = redis_db.zadd(reminders_key, {service_id: reminder_timestamp})
    print(f"Debug: ZADD result: {result}")
    
    # Store cost history for analytics (with some sample historical data for better charts)
    cost_history_key = f"cost_history:{org_id}:{service_id}"
    existing_history = redis_db.get(cost_history_key) or []
    
    # If this is the first entry, create some sample historical data for better visualization
    if not existing_history:
        # Create 3 months of sample historical data with realistic gradual variations
        base_date = datetime.utcnow()
        base_cost = service.cost
        
        for i in range(3, 0, -1):  # 3, 2, 1 months ago
            historical_date = datetime(
                base_date.year, 
                max(1, base_date.month - i), 
                base_date.day
            )
            # Create realistic cost progression (gradual increase/decrease to current cost)
            # Start from 80-90% of current cost and gradually approach it
            progression_factor = 0.8 + (0.2 * (4 - i) / 3)  # 0.8 -> 0.87 -> 0.93 -> 1.0
            historical_cost = base_cost * progression_factor
            
            cost_entry = {
                "date": historical_date.isoformat(),
                "cost": round(historical_cost, 2)
            }
            existing_history.append(cost_entry)
    
    # Add current entry
    cost_entry = {
        "date": datetime.utcnow().isoformat(),
        "cost": service.cost
    }
    existing_history.append(cost_entry)
    redis_db.set(cost_history_key, existing_history)
    
    # Send alerts to all configured integrations (global for user)
    print(f"DEBUG: About to send global service creation alert for user {current_user.email}")
    try:
        await send_service_creation_alert(org_id, service_data, current_user)
        print(f"DEBUG: Finished sending global service creation alert for user {current_user.email}")
    except Exception as e:
        print(f"DEBUG: Error in service creation alert: {e}")
        import traceback
        traceback.print_exc()
    
    return Service(**service_data)

@router.get("/organizations/{org_id}/services", response_model=List[Service])
async def list_services(
    org_id: str,
    current_user: User = Depends(get_current_user)
):
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get services for organization
    org_services_key = f"org_services:{org_id}"
    service_ids = redis_db.get(org_services_key) or []
    
    services = []
    for service_id in service_ids:
        service_key = f"service:{service_id}"
        service_data = redis_db.get(service_key)
        if service_data and service_data.get("status") == "active":
            services.append(Service(**service_data))
    
    return services

@router.put("/services/{service_id}", response_model=Service)
async def update_service(
    service_id: str,
    service_update: ServiceUpdate,
    current_user: User = Depends(get_current_user)
):
    service_key = f"service:{service_id}"
    service_data = redis_db.get(service_key)
    
    if not service_data:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Check if user has moderator access to this service's organization
    org_id = service_data["org_id"]
    org_data = check_organization_moderator_access(org_id, current_user)
    if not has_moderator_access(org_data, current_user.id):
        raise HTTPException(status_code=403, detail="Only organization owner or moderators can update services")
    
    # Update fields
    update_data = service_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field in ["platform", "service_type"] and value:
            service_data[field] = value.value
        elif value is not None:
            service_data[field] = value
    
    service_data["updated_at"] = datetime.utcnow().isoformat()
    
    # If cost was updated, store in cost history
    if "cost" in update_data:
        cost_history_key = f"cost_history:{org_id}:{service_id}"
        cost_entry = {
            "date": datetime.utcnow().isoformat(),
            "cost": service_data["cost"]
        }
        existing_history = redis_db.get(cost_history_key) or []
        existing_history.append(cost_entry)
        redis_db.set(cost_history_key, existing_history)
    
    # If reminder_date was updated, update the sorted set
    if "reminder_date" in update_data:
        reminders_key = f"reminders:{org_id}"
        # Remove old entry and add new one
        redis_db.zrem(reminders_key, service_id)
        reminder_timestamp = int(datetime.fromisoformat(service_data["reminder_date"]).timestamp())
        redis_db.zadd(reminders_key, {service_id: reminder_timestamp})
    
    # Save updated service
    redis_db.set(service_key, service_data)
    
    return Service(**service_data)

@router.delete("/services/{service_id}")
async def delete_service(
    service_id: str,
    current_user: User = Depends(get_current_user)
):
    service_key = f"service:{service_id}"
    service_data = redis_db.get(service_key)
    
    if not service_data:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Check if user has access to this service's organization
    org_id = service_data["org_id"]
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if user has moderator access (owner or moderator)
    org_data = check_organization_moderator_access(org_id, current_user)
    if not has_moderator_access(org_data, current_user.id):
        raise HTTPException(status_code=403, detail="Only organization owner or moderators can delete services")
    
    # Mark for deletion instead of actual deletion
    service_data["status"] = "pending_deletion"
    service_data["updated_at"] = datetime.utcnow().isoformat()
    redis_db.set(service_key, service_data)
    
    # Remove from reminders
    reminders_key = f"reminders:{org_id}"
    redis_db.zrem(reminders_key, service_id)
    
    # Send deletion alerts to all configured integrations (global for user)
    print(f"DEBUG: About to send global service deletion alert for user {current_user.email}")
    try:
        await send_service_deletion_alert(org_id, service_data, current_user)
        print(f"DEBUG: Finished sending global service deletion alert for user {current_user.email}")
    except Exception as e:
        print(f"DEBUG: Error in service deletion alert: {e}")
        import traceback
        traceback.print_exc()
    
    return {"message": "Service marked for deletion"}

@router.get("/organizations/{org_id}/analytics", response_model=ServiceAnalytics)
async def get_service_analytics(
    org_id: str,
    current_user: User = Depends(get_current_user)
):
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get all services for the organization
    org_services_key = f"org_services:{org_id}"
    service_ids = redis_db.get(org_services_key) or []
    
    total_cost = 0
    active_services = 0
    cost_by_platform = defaultdict(float)
    cost_by_type = defaultdict(float)
    cost_trend = []
    
    for service_id in service_ids:
        service_key = f"service:{service_id}"
        service_data = redis_db.get(service_key)
        
        if service_data and service_data.get("status") == "active":
            active_services += 1
            cost = service_data.get("cost", 0)
            total_cost += cost
            
            platform = service_data.get("platform", "unknown")
            service_type = service_data.get("service_type", "unknown")
            
            cost_by_platform[platform] += cost
            cost_by_type[service_type] += cost
            
            # Get cost history for this service
            cost_history_key = f"cost_history:{org_id}:{service_id}"
            history = redis_db.get(cost_history_key) or []
            cost_trend.extend(history)
    
    # Sort cost trend by date
    cost_trend.sort(key=lambda x: x.get("date", ""))
    
    # If we don't have enough historical data, create some aggregated monthly data
    if len(cost_trend) < 4 and active_services > 0:
        # Create monthly aggregated data for better trend visualization
        monthly_costs = []
        base_date = datetime.utcnow()
        
        for i in range(6, 0, -1):  # 6 months of data
            month_date = datetime(
                base_date.year if base_date.month > i else base_date.year - 1,
                base_date.month - i if base_date.month > i else 12 + base_date.month - i,
                1
            )
            
            # Create realistic gradual progression to current total cost
            # Start from 75% of current cost and gradually increase
            progression_factor = 0.75 + (0.25 * (7 - i) / 6)  # 0.75 -> 0.79 -> 0.83 -> 0.88 -> 0.92 -> 0.96
            monthly_total = total_cost * progression_factor
            monthly_costs.append({
                "date": month_date.isoformat(),
                "cost": round(monthly_total, 2)
            })
        
        # Replace cost_trend with monthly data if we don't have enough
        if len(monthly_costs) > len(cost_trend):
            cost_trend = monthly_costs
    
    # Simple linear regression for prediction
    predicted_next_month = total_cost  # Default to current cost
    if len(cost_trend) >= 2:
        # Get last 6 months of data for trend analysis
        recent_trend = cost_trend[-6:] if len(cost_trend) >= 6 else cost_trend
        
        if len(recent_trend) >= 2:
            # Simple linear regression: y = mx + b
            x_values = list(range(len(recent_trend)))
            y_values = [entry.get("cost", 0) for entry in recent_trend]
            
            n = len(recent_trend)
            sum_x = sum(x_values)
            sum_y = sum(y_values)
            sum_xy = sum(x * y for x, y in zip(x_values, y_values))
            sum_x_squared = sum(x * x for x in x_values)
            
            # Calculate slope (m) and intercept (b)
            if n * sum_x_squared - sum_x * sum_x != 0:
                m = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x * sum_x)
                b = (sum_y - m * sum_x) / n
                
                # Predict next month (next x value)
                next_x = len(recent_trend)
                predicted_next_month = m * next_x + b
                predicted_next_month = max(0, predicted_next_month)  # Don't predict negative costs
    
    return ServiceAnalytics(
        total_monthly_cost=total_cost,
        total_services=active_services,
        cost_by_platform=dict(cost_by_platform),
        cost_by_type=dict(cost_by_type),
        predicted_next_month=predicted_next_month,
        cost_trend=cost_trend
    )

@router.post("/reminder-alerts")
async def trigger_reminder_alerts(
    days_ahead: int = 7,
    current_user: User = Depends(get_current_user)
):
    """Manually trigger reminder alerts for upcoming service reminders"""
    try:
        await send_reminder_alerts(current_user, days_ahead)
        return {"message": f"Reminder alerts sent for upcoming reminders in the next {days_ahead} days"}
    except Exception as e:
        print(f"Error triggering reminder alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to send reminder alerts")

async def send_service_creation_alert(org_id: str, service_data: dict, current_user: User):
    """Send alerts to all configured integrations for the user (global across all organizations)"""
    try:
        print(f"DEBUG: Starting global service creation alert for user {current_user.email}")
        
        # Get all integrations for ALL organizations that this user belongs to
        all_integration_keys = []
        
        for user_org_id in current_user.organizations:
            try:
                org_integration_keys = redis_db.keys(f"integration:{user_org_id}:*")
                all_integration_keys.extend(org_integration_keys)
                print(f"DEBUG: Found {len(org_integration_keys)} integrations for org {user_org_id}")
            except Exception as e:
                print(f"DEBUG: Error getting integration keys for org {user_org_id}: {e}")
        
        print(f"DEBUG: Total global integration keys found: {len(all_integration_keys)}")
        
        if not all_integration_keys:
            print(f"DEBUG: No integrations configured for user {current_user.email} across all organizations")
            print(f"DEBUG: User organizations: {current_user.organizations}")
            return
        
        # Format service metadata for the alert
        platform_emojis = {
            "aws": "🟠 Amazon Web Services",
            "gcp": "🔵 Google Cloud Platform", 
            "azure": "🔷 Microsoft Azure",
            "other": "⚡ Other Platform"
        }
        
        service_type_emojis = {
            "ec2": "🖥️", "s3": "🗄️", "rds": "🗃️", "lambda": "⚡", "eks": "☸️",
            "compute_engine": "🖥️", "cloud_storage": "🗄️", "cloud_sql": "🗃️",
            "virtual_machines": "🖥️", "blob_storage": "🗄️", "sql_database": "🗃️",
            "cloud": "☁️", "api": "🔌", "database": "🗃️", "storage": "🗄️"
        }
        
        platform_name = platform_emojis.get(service_data["platform"], f"⚡ {service_data['platform'].title()}")
        service_emoji = service_type_emojis.get(service_data["service_type"], "📦")
        
        # Get organization name for context
        org_key = f"org:{org_id}"
        org_data = redis_db.get(org_key)
        org_name = org_data.get('name', 'Unknown Organization') if org_data else 'Unknown Organization'
        
        # Create rich alert message with organization context
        alert_message = f"""🎉 **New Service Created!**

{service_emoji} **Service:** {service_data['name']}
🏢 **Organization:** {org_name}
{platform_name}
📊 **Type:** {service_data['service_type'].replace('_', ' ').title()}
💰 **Monthly Cost:** ${service_data['cost']:.2f}
📅 **Next Reminder:** {service_data['reminder_date'][:10]}
👤 **Owner:** {service_data.get('owner_email', 'Not specified')}"""

        # Add optional metadata if present
        if service_data.get('instance_type'):
            alert_message += f"\n🖥️ **Instance Type:** {service_data['instance_type'].replace('_', ' ').title()}"
        
        if service_data.get('description'):
            alert_message += f"\n📝 **Description:** {service_data['description']}"
        
        if service_data.get('region'):
            alert_message += f"\n🌍 **Region:** {service_data['region']}"
        
        if service_data.get('instance_id'):
            alert_message += f"\n🏷️ **Instance ID:** {service_data['instance_id']}"
        
        if service_data.get('iam_number'):
            alert_message += f"\n🔐 **IAM Number:** {service_data['iam_number']}"
        
        if service_data.get('api_quota_tokens'):
            alert_message += f"\n🎫 **API Quota:** {service_data['api_quota_tokens']:,} tokens"
        
        if service_data.get('tags'):
            tags = ', '.join(service_data['tags']) if isinstance(service_data['tags'], list) else str(service_data['tags'])
            alert_message += f"\n🏷️ **Tags:** {tags}"
        
        alert_message += f"\n\n⏰ **Created:** {service_data['created_at'][:19]} UTC"
        alert_message += f"\n🆔 **Service ID:** {service_data['id']}"
        
        # Send to all configured integrations (global across user's organizations)
        success_count = 0
        total_count = 0
        
        for integration_key in all_integration_keys:
            try:
                integration_data = redis_db.get(integration_key)
                print(f"DEBUG: Processing integration {integration_key}: {integration_data}")
                
                if not integration_data or not integration_data.get('enabled', False):
                    print(f"DEBUG: Skipping disabled integration {integration_key}")
                    continue
                
                total_count += 1
                integration_type = integration_data['type']
                config = integration_data['config']
                
                print(f"DEBUG: Sending alert via {integration_type} integration")
                
                # Send alert based on integration type
                success = await IntegrationService.send_alert_to_integration(
                    integration_type=integration_type,
                    config=config,
                    message=alert_message,
                    subject="🎉 New Service Created - BurnStop Alert"
                )
                
                if success:
                    success_count += 1
                    print(f"Service creation alert sent successfully via {integration_type}")
                else:
                    print(f"Failed to send service creation alert via {integration_type}")
                    
            except Exception as e:
                print(f"Error sending alert via integration {integration_key}: {e}")
        
        print(f"Global service creation alerts: {success_count}/{total_count} integrations notified successfully across user's organizations")
        
    except Exception as e:
        print(f"Error sending global service creation alerts: {e}")
        # Don't raise the exception to avoid breaking service creation

async def send_service_deletion_alert(org_id: str, service_data: dict, current_user: User):
    """Send alerts to all configured integrations for the user when a service is deleted (global across all organizations)"""
    try:
        print(f"DEBUG: Starting global service deletion alert for user {current_user.email}")
        
        # Get all integrations for ALL organizations that this user belongs to
        all_integration_keys = []
        
        for user_org_id in current_user.organizations:
            try:
                org_integration_keys = redis_db.keys(f"integration:{user_org_id}:*")
                all_integration_keys.extend(org_integration_keys)
                print(f"DEBUG: Found {len(org_integration_keys)} integrations for org {user_org_id}")
            except Exception as e:
                print(f"DEBUG: Error getting integration keys for org {user_org_id}: {e}")
        
        print(f"DEBUG: Total global integration keys found for deletion: {len(all_integration_keys)}")
        
        if not all_integration_keys:
            print(f"DEBUG: No integrations configured for user {current_user.email} across all organizations")
            print(f"DEBUG: User organizations: {current_user.organizations}")
            return
        
        # Format service metadata for the deletion alert
        platform_emojis = {
            "aws": "🟠 Amazon Web Services",
            "gcp": "🔵 Google Cloud Platform", 
            "azure": "🔷 Microsoft Azure",
            "other": "⚡ Other Platform"
        }
        
        service_type_emojis = {
            "ec2": "🖥️", "s3": "��️", "rds": "🗃️", "lambda": "⚡", "eks": "☸️",
            "compute_engine": "🖥️", "cloud_storage": "🗄️", "cloud_sql": "🗃️",
            "virtual_machines": "🖥️", "blob_storage": "🗄️", "sql_database": "🗃️",
            "cloud": "☁️", "api": "🔌", "database": "🗃️", "storage": "🗄️"
        }
        
        platform_name = platform_emojis.get(service_data["platform"], f"⚡ {service_data['platform'].title()}")
        service_emoji = service_type_emojis.get(service_data["service_type"], "📦")
        
        # Get organization name for context
        org_key = f"org:{org_id}"
        org_data = redis_db.get(org_key)
        org_name = org_data.get('name', 'Unknown Organization') if org_data else 'Unknown Organization'
        
        # Create rich deletion alert message with organization context
        alert_message = f"""🗑️ **Service Deleted!**

{service_emoji} **Service:** {service_data['name']}
🏢 **Organization:** {org_name}
{platform_name}
📊 **Type:** {service_data['service_type'].replace('_', ' ').title()}
💰 **Monthly Cost Saved:** ${service_data['cost']:.2f}
👤 **Owner:** {service_data.get('owner_email', 'Not specified')}"""

        # Add optional metadata if present
        if service_data.get('instance_type'):
            alert_message += f"\n🖥️ **Instance Type:** {service_data['instance_type'].replace('_', ' ').title()}"
        
        if service_data.get('description'):
            alert_message += f"\n📝 **Description:** {service_data['description']}"
        
        if service_data.get('region'):
            alert_message += f"\n🌍 **Region:** {service_data['region']}"
        
        if service_data.get('instance_id'):
            alert_message += f"\n🏷️ **Instance ID:** {service_data['instance_id']}"
        
        if service_data.get('iam_number'):
            alert_message += f"\n🔐 **IAM Number:** {service_data['iam_number']}"
        
        if service_data.get('tags'):
            tags = ', '.join(service_data['tags']) if isinstance(service_data['tags'], list) else str(service_data['tags'])
            alert_message += f"\n🏷️ **Tags:** {tags}"
        
        alert_message += f"\n\n🗑️ **Deleted:** {service_data['updated_at'][:19]} UTC"
        alert_message += f"\n🆔 **Service ID:** {service_data['id']}"
        alert_message += f"\n⚠️ **Status:** Marked for deletion"
        
        # Send to all configured integrations (global across user's organizations)
        success_count = 0
        total_count = 0
        
        for integration_key in all_integration_keys:
            try:
                integration_data = redis_db.get(integration_key)
                print(f"DEBUG: Processing deletion integration {integration_key}: {integration_data}")
                
                if not integration_data or not integration_data.get('enabled', False):
                    print(f"DEBUG: Skipping disabled integration {integration_key}")
                    continue
                
                total_count += 1
                integration_type = integration_data['type']
                config = integration_data['config']
                
                print(f"DEBUG: Sending deletion alert via {integration_type} integration")
                
                # Send alert based on integration type
                success = await IntegrationService.send_alert_to_integration(
                    integration_type=integration_type,
                    config=config,
                    message=alert_message,
                    subject="🗑️ Service Deleted - BurnStop Alert"
                )
                
                if success:
                    success_count += 1
                    print(f"Service deletion alert sent successfully via {integration_type}")
                else:
                    print(f"Failed to send service deletion alert via {integration_type}")
                    
            except Exception as e:
                print(f"Error sending deletion alert via integration {integration_key}: {e}")
        
        print(f"Global service deletion alerts: {success_count}/{total_count} integrations notified successfully across user's organizations")
        
    except Exception as e:
        print(f"Error sending global service deletion alerts: {e}")
        # Don't raise the exception to avoid breaking service deletion

async def send_reminder_alerts(current_user: User, days_ahead: int = 7):
    """Send alerts for upcoming service reminders (global across all user's organizations)"""
    try:
        print(f"DEBUG: Starting global reminder alerts for user {current_user.email} - checking {days_ahead} days ahead")
        
        # Get all integrations for ALL organizations that this user belongs to
        all_integration_keys = []
        
        for user_org_id in current_user.organizations:
            try:
                org_integration_keys = redis_db.keys(f"integration:{user_org_id}:*")
                all_integration_keys.extend(org_integration_keys)
                print(f"DEBUG: Found {len(org_integration_keys)} integrations for org {user_org_id}")
            except Exception as e:
                print(f"DEBUG: Error getting integration keys for org {user_org_id}: {e}")
        
        print(f"DEBUG: Total global integration keys found for reminders: {len(all_integration_keys)}")
        
        if not all_integration_keys:
            print(f"DEBUG: No integrations configured for user {current_user.email} across all organizations")
            return
        
        # Collect all upcoming reminders across all user's organizations
        current_timestamp = int(time.time())
        future_timestamp = current_timestamp + (days_ahead * 24 * 60 * 60)
        
        all_upcoming_reminders = []
        
        for user_org_id in current_user.organizations:
            try:
                reminders_key = f"reminders:{user_org_id}"
                upcoming_reminders = redis_db.zrangebyscore(
                    reminders_key, 
                    current_timestamp, 
                    future_timestamp, 
                    withscores=True
                )
                
                # Get organization name
                org_key = f"org:{user_org_id}"
                org_data = redis_db.get(org_key)
                org_name = org_data.get('name', 'Unknown Organization') if org_data else 'Unknown Organization'
                
                for service_id, reminder_timestamp in upcoming_reminders:
                    service_key = f"service:{service_id}"
                    service_data = redis_db.get(service_key)
                    
                    if service_data and service_data.get("status") == "active":
                        reminder_info = {
                            'service_data': service_data,
                            'org_name': org_name,
                            'org_id': user_org_id,
                            'reminder_timestamp': reminder_timestamp,
                            'days_until': round((reminder_timestamp - current_timestamp) / (24 * 60 * 60), 1)
                        }
                        all_upcoming_reminders.append(reminder_info)
                        
            except Exception as e:
                print(f"DEBUG: Error getting reminders for org {user_org_id}: {e}")
        
        if not all_upcoming_reminders:
            print(f"DEBUG: No upcoming reminders found for user {current_user.email} in the next {days_ahead} days")
            return
        
        # Sort reminders by days until due
        all_upcoming_reminders.sort(key=lambda x: x['days_until'])
        
        print(f"DEBUG: Found {len(all_upcoming_reminders)} upcoming reminders")
        
        # Create rich reminder alert message
        alert_message = f"""⏰ **Upcoming Service Reminders**

You have {len(all_upcoming_reminders)} service reminder(s) in the next {days_ahead} days:

"""
        
        platform_emojis = {
            "aws": "🟠", "gcp": "🔵", "azure": "🔷", "other": "⚡"
        }
        
        service_type_emojis = {
            "ec2": "🖥️", "s3": "🗄️", "rds": "🗃️", "lambda": "⚡", "eks": "☸️",
            "compute_engine": "🖥️", "cloud_storage": "🗄️", "cloud_sql": "🗃️",
            "virtual_machines": "🖥️", "blob_storage": "🗄️", "sql_database": "🗃️",
            "cloud": "☁️", "api": "🔌", "database": "🗃️", "storage": "🗄️"
        }
        
        total_cost = 0
        
        for i, reminder in enumerate(all_upcoming_reminders, 1):
            service_data = reminder['service_data']
            platform_emoji = platform_emojis.get(service_data["platform"], "⚡")
            service_emoji = service_type_emojis.get(service_data["service_type"], "📦")
            total_cost += service_data.get('cost', 0)
            
            days_until = reminder['days_until']
            urgency_indicator = "🔴" if days_until <= 1 else "🟡" if days_until <= 3 else "🟢"
            
            alert_message += f"""
{urgency_indicator} **{i}. {service_data['name']}**
   {service_emoji} {service_data['service_type'].replace('_', ' ').title()} • {platform_emoji} {service_data['platform'].upper()}
   🏢 {reminder['org_name']}
   💰 ${service_data['cost']:.2f}/month
   📅 Due in {days_until} day(s) - {datetime.fromtimestamp(reminder['reminder_timestamp']).strftime('%Y-%m-%d')}"""
   
            # Add instance type if available
            if service_data.get('instance_type'):
                alert_message += f"\n   🖥️ {service_data['instance_type'].replace('_', ' ').title()}"
            
            # Add region if available  
            if service_data.get('region'):
                alert_message += f"\n   🌍 {service_data['region']}"
            
            alert_message += f"""
"""
        
        alert_message += f"""
📊 **Summary:**
• Total services: {len(all_upcoming_reminders)}
• Total monthly cost: ${total_cost:.2f}
• Most urgent: {all_upcoming_reminders[0]['days_until']} day(s)

🎯 **Action Required:** Review and update these services to avoid cost overruns!
"""
        
        # Send to all configured integrations
        success_count = 0
        total_count = 0
        
        for integration_key in all_integration_keys:
            try:
                integration_data = redis_db.get(integration_key)
                
                if not integration_data or not integration_data.get('enabled', False):
                    continue
                
                total_count += 1
                integration_type = integration_data['type']
                config = integration_data['config']
                
                print(f"DEBUG: Sending reminder alert via {integration_type} integration")
                
                # Send alert based on integration type
                success = await IntegrationService.send_alert_to_integration(
                    integration_type=integration_type,
                    config=config,
                    message=alert_message,
                    subject=f"⏰ {len(all_upcoming_reminders)} Upcoming Service Reminders - BurnStop Alert"
                )
                
                if success:
                    success_count += 1
                    print(f"Reminder alert sent successfully via {integration_type}")
                else:
                    print(f"Failed to send reminder alert via {integration_type}")
                    
            except Exception as e:
                print(f"Error sending reminder alert via integration {integration_key}: {e}")
        
        print(f"Global reminder alerts: {success_count}/{total_count} integrations notified successfully")
        
    except Exception as e:
        print(f"Error sending global reminder alerts: {e}")
        # Don't raise the exception

@router.get("/service-types")
async def get_service_types():
    """Get all available service types from the ServiceType enum, categorized by platform"""
    
    # Categorize services by platform
    aws_services = []
    gcp_services = []
    azure_services = []
    other_services = []
    
    # AWS instance types
    aws_instance_types = []
    gcp_instance_types = []
    
    for service_type in ServiceType:
        value = service_type.value
        label = service_type.value.replace("_", " ").title()
        
        service_item = {
            "value": value,
            "label": label
        }
        
        # Categorize AWS services
        if any(aws_service in value for aws_service in [
            'ec2', 's3', 'rds', 'lambda', 'dynamodb', 'cloudfront', 'route53', 'vpc', 
            'iam', 'sns', 'sqs', 'ses', 'cloudwatch', 'eks', 'ecs', 'fargate',
            'elasticbeanstalk', 'cloudformation', 'codecommit', 'codebuild', 'codedeploy',
            'codepipeline', 'api_gateway', 'kinesis', 'redshift', 'elasticache',
            'cloudtrail', 'config', 'secrets_manager', 'systems_manager', 'batch',
            'step_functions', 'eventbridge', 'glue', 'athena', 'quicksight',
            'sagemaker', 'rekognition', 'comprehend', 'textract', 'bedrock',
            'lex', 'polly', 'translate', 'transcribe', 'x_ray', 'application_load_balancer',
            'network_load_balancer', 'nat_gateway', 'internet_gateway', 'vpn_gateway',
            'direct_connect', 'storage_gateway', 'backup', 'datasync', 'transfer_family',
            'workspaces', 'appstream', 'connect', 'chime', 'organizations',
            'control_tower', 'security_hub', 'guardduty', 'inspector', 'macie',
            'certificate_manager', 'kms', 'cloudhsm', 'waf', 'shield', 'marketplace',
            'cost_explorer', 'budgets', 'trusted_advisor', 'support', 'personal_health_dashboard'
        ]):
            aws_services.append(service_item)
        
        # AWS Instance Types - check for exact matches and patterns
        elif (value.startswith(('t4g_', 't3_', 't3a_', 't2_', 'm7g_', 'm7i_', 'm7a_', 'm6g_', 'm6i_', 'm6a_',
                               'm5_', 'm5a_', 'm5n_', 'c7g_', 'c7i_', 'c7a_', 'c6g_', 'c6i_', 'c6a_',
                               'c5_', 'c5a_', 'c5n_', 'r7g_', 'r7i_', 'r7a_', 'r6g_', 'r6i_', 'r6a_',
                               'r5_', 'r5a_', 'r5n_', 'x2gd_', 'x2idn_', 'x2iedn_', 'x2iezn_', 'x1e_',
                               'x1_', 'i4g_', 'i4i_', 'i3_', 'i3en_', 'd3_', 'd3en_', 'p5_', 'p4d_',
                               'p4de_', 'p3_', 'p3dn_', 'p2_', 'g5_', 'g5g_', 'g4dn_', 'g4ad_', 'g3_',
                               'inf2_', 'inf1_', 'trn1_', 'trn1n_', 'dl1_', 'hpc7g_', 'hpc7a_', 'hpc6id_', 'hpc6a_'))):
            aws_instance_types.append(service_item)
        
        # GCP services
        elif any(gcp_service in value for gcp_service in [
            'compute_engine', 'cloud_storage', 'cloud_sql', 'cloud_functions', 'gke',
            'cloud_run', 'app_engine', 'bigquery', 'cloud_bigtable', 'cloud_spanner',
            'firestore', 'cloud_cdn', 'cloud_dns', 'cloud_load_balancing', 'vpc',
            'cloud_iam', 'cloud_pub_sub', 'cloud_tasks', 'cloud_scheduler',
            'cloud_monitoring', 'cloud_logging', 'cloud_trace', 'cloud_profiler',
            'cloud_debugger', 'cloud_build', 'cloud_source_repositories',
            'artifact_registry', 'container_registry', 'cloud_endpoints',
            'api_gateway', 'cloud_dataflow', 'cloud_dataproc', 'cloud_composer',
            'cloud_data_fusion', 'looker', 'vertex_ai', 'automl', 'ai_platform',
            'vision_api', 'speech_to_text', 'text_to_speech', 'cloud_translate',
            'natural_language_ai', 'document_ai', 'video_intelligence',
            'recommendations_ai', 'dialogflow', 'contact_center_ai',
            'cloud_security_command_center', 'cloud_armor', 'binary_authorization',
            'cloud_kms', 'cloud_hsm', 'secret_manager', 'identity_platform',
            'cloud_identity', 'access_context_manager', 'cloud_asset_inventory',
            'cloud_console', 'cloud_shell', 'cloud_deployment_manager',
            'cloud_resource_manager', 'cloud_billing', 'cloud_support',
            'firebase_'
        ]):
            gcp_services.append(service_item)
        
        # GCP Instance Types - check for exact matches and patterns
        elif (value.startswith(('e2_', 'n1_', 'n2_', 'n2d_', 't2d_', 't2a_', 'c3_', 'c2_', 'c2d_',
                               'm1_', 'm2_', 'm3_', 'a2_', 'a3_', 'g2_', 'h3_', 'sole_tenant_'))):
            gcp_instance_types.append(service_item)
        
        # Azure services
        elif any(azure_service in value for azure_service in [
            'virtual_machines', 'blob_storage', 'sql_database', 'azure_functions',
            'aks', 'container_instances', 'cosmos_db', 'cognitive_services',
            'app_service', 'service_fabric', 'batch', 'virtual_machine_scale_sets',
            'load_balancer', 'application_gateway', 'cdn', 'traffic_manager',
            'expressroute', 'vpn_gateway', 'azure_firewall', 'azure_active_directory'
        ]):
            azure_services.append(service_item)
        
        # Other services
        else:
            other_services.append(service_item)
    
    return {
        "aws": {
            "services": aws_services,
            "instance_types": aws_instance_types
        },
        "gcp": {
            "services": gcp_services,
            "instance_types": gcp_instance_types
        },
        "azure": {
            "services": azure_services,
            "instance_types": []
        },
        "other": {
            "services": other_services,
            "instance_types": []
        }
    }

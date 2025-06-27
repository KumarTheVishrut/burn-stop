from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import uuid
from datetime import datetime
import json
import os
import requests

from models.organization import Organization, OrganizationCreate, AddUserToOrg, UpdateOrganizationBudget, AddModeratorToOrg, RemoveModeratorFromOrg
from models.user import User
from routers.auth import get_current_user
from utils.redis_db import redis_db

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.post("/", response_model=Organization)
async def create_organization(
    org: OrganizationCreate,
    current_user: User = Depends(get_current_user)
):
    # Create organization
    org_id = str(uuid.uuid4())
    org_data = {
        "id": org_id,
        "name": org.name,
        "budget": org.budget,
        "owner_id": current_user.id,
        "members": [current_user.id],
        "moderators": [],  # Initialize empty moderators list
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Save organization
    org_key = f"org:{org_id}"
    redis_db.set(org_key, org_data)
    
    # Add organization to user's list
    user_key = f"user:{current_user.id}"
    user_data = redis_db.get(user_key)
    if user_data:
        user_data["organizations"].append(org_id)
        redis_db.set(user_key, user_data)
    
    return Organization(**org_data)

@router.get("/", response_model=List[Organization])
async def list_organizations(current_user: User = Depends(get_current_user)):
    organizations = []
    for org_id in current_user.organizations:
        org_key = f"org:{org_id}"
        org_data = redis_db.get(org_key)
        if org_data:
            organizations.append(Organization(**org_data))
    return organizations

@router.get("/{org_id}", response_model=Organization)
async def get_organization(
    org_id: str,
    current_user: User = Depends(get_current_user)
):
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Ensure backwards compatibility with existing organizations
    if "moderators" not in org_data:
        org_data["moderators"] = []
        redis_db.set(org_key, org_data)  # Update the stored data
    
    return Organization(**org_data)

@router.put("/{org_id}/budget")
async def update_organization_budget(
    org_id: str,
    budget_data: UpdateOrganizationBudget,
    current_user: User = Depends(get_current_user)
):
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if not has_moderator_access(org_data, current_user.id):
        raise HTTPException(status_code=403, detail="Only organization owner or moderators can update budget")
    
    # Update budget
    org_data["budget"] = budget_data.budget
    redis_db.set(org_key, org_data)
    
    return {"message": "Budget updated successfully", "budget": budget_data.budget}

@router.post("/{org_id}/users")
async def add_user_to_organization(
    org_id: str,
    user_data: AddUserToOrg,
    current_user: User = Depends(get_current_user)
):
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if not has_moderator_access(org_data, current_user.id):
        raise HTTPException(status_code=403, detail="Only organization owner or moderators can add users")
    
    # Find user by email
    email_key = f"email:{user_data.user_email}"
    user_id = redis_db.get(email_key)
    
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user is already a member
    if user_id in org_data["members"]:
        raise HTTPException(status_code=400, detail="User is already a member")
    
    # Add user to organization
    org_data["members"].append(user_id)
    redis_db.set(org_key, org_data)
    
    # Add organization to user's list
    user_key = f"user:{user_id}"
    user_data_obj = redis_db.get(user_key)
    if user_data_obj:
        user_data_obj["organizations"].append(org_id)
        redis_db.set(user_key, user_data_obj)
    
    return {"message": "User added successfully"}

@router.delete("/{org_id}")
async def delete_organization(
    org_id: str,
    current_user: User = Depends(get_current_user)
):
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if not is_owner(org_data, current_user.id):
        raise HTTPException(status_code=403, detail="Only organization owner can delete organization")
    
    # Remove organization from all members' lists
    for member_id in org_data["members"]:
        user_key = f"user:{member_id}"
        user_data = redis_db.get(user_key)
        if user_data and org_id in user_data["organizations"]:
            user_data["organizations"].remove(org_id)
            redis_db.set(user_key, user_data)
    
    # Delete all services associated with this organization
    services_pattern = f"service:*"
    for service_key in redis_db.redis_client.scan_iter(match=services_pattern):
        service_data = redis_db.get(service_key)
        if service_data and service_data.get("organization_id") == org_id:
            redis_db.delete(service_key)
    
    # Delete all reminders associated with this organization
    reminders_pattern = f"reminder:*"
    for reminder_key in redis_db.redis_client.scan_iter(match=reminders_pattern):
        reminder_data = redis_db.get(reminder_key)
        if reminder_data and reminder_data.get("organization_id") == org_id:
            redis_db.delete(reminder_key)
    
    # Delete the organization itself
    redis_db.delete(org_key)
    
    return {"message": "Organization deleted successfully"}

@router.delete("/{org_id}/users/{user_id}")
async def remove_user_from_organization(
    org_id: str,
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if not has_moderator_access(org_data, current_user.id):
        raise HTTPException(status_code=403, detail="Only organization owner or moderators can remove users")
    
    # Can't remove the owner
    if user_id == org_data["owner_id"]:
        raise HTTPException(status_code=400, detail="Cannot remove organization owner")
    
    # Remove user from organization
    if user_id in org_data["members"]:
        org_data["members"].remove(user_id)
        redis_db.set(org_key, org_data)
        
        # Remove organization from user's list
        user_key = f"user:{user_id}"
        user_data = redis_db.get(user_key)
        if user_data and org_id in user_data["organizations"]:
            user_data["organizations"].remove(org_id)
            redis_db.set(user_key, user_data)
    
    return {"message": "User removed successfully"}

# OpenAI API Key Management
@router.post("/{org_id}/api-key/openai")
async def save_openai_api_key(
    org_id: str,
    api_key_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Save OpenAI API key for an organization (owner only)"""
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if org_data["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only organization owner can manage OpenAI API keys")
    
    api_key = api_key_data.get("api_key")
    if not api_key:
        raise HTTPException(status_code=400, detail="API key is required")
    
    # Save API key associated with organization
    api_key_storage = f"openai_key:{org_id}"
    redis_db.set(api_key_storage, {"api_key": api_key, "created_at": datetime.utcnow().isoformat()})
    
    return {"message": "OpenAI API key saved successfully"}

@router.get("/{org_id}/api-key/openai/status")
async def get_openai_api_key_status(
    org_id: str, 
    current_user: User = Depends(get_current_user)
):
    """Check if organization has saved an OpenAI API key (owner only)"""
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if org_data["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only organization owner can view OpenAI API key status")
    
    api_key_storage = f"openai_key:{org_id}"
    api_key_data = redis_db.get(api_key_storage)
    
    return {
        "has_key": api_key_data is not None,
        "created_at": api_key_data.get("created_at") if api_key_data else None
    }

@router.delete("/{org_id}/api-key/openai")
async def delete_openai_api_key(
    org_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete saved OpenAI API key (owner only)"""
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if org_data["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only organization owner can delete OpenAI API keys")
    
    api_key_storage = f"openai_key:{org_id}"
    redis_db.delete(api_key_storage)
    
    return {"message": "OpenAI API key deleted successfully"}

# AI Insights
@router.post("/{org_id}/ai-insights")
async def get_ai_insights(
    org_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get AI insights for organization services using OpenAI"""
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get organization data first
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Check if current user is owner of the organization (only owners can generate AI insights)
    if org_data["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only organization owner can generate AI insights")
    
    # Get organization's OpenAI API key
    api_key_storage = f"openai_key:{org_id}"
    api_key_data = redis_db.get(api_key_storage)
    
    print(f"Debug: Looking for API key at {api_key_storage}")
    print(f"Debug: API key data found: {api_key_data is not None}")
    
    if not api_key_data:
        raise HTTPException(status_code=400, detail="OpenAI API key not configured for this organization. Please add your API key in the integration settings.")
    
    # Get all services for this organization using the correct field name
    services = []
    services_pattern = f"service:*"
    for service_key in redis_db.redis_client.scan_iter(match=services_pattern):
        service_data = redis_db.get(service_key)
        # Services are stored with "org_id" field, not "organization_id"
        if service_data and service_data.get("org_id") == org_id and service_data.get("status") == "active":
            services.append(service_data)
    
    print(f"Debug: Found {len(services)} services for organization {org_id}")
    
    if not services:
        raise HTTPException(status_code=400, detail="No services found for this organization")
    
    try:
        # Prepare data for OpenAI
        services_summary = []
        total_cost = 0
        
        for service in services:
            service_info = {
                "name": service.get("name"),
                "platform": service.get("platform"),
                "service_type": service.get("service_type"),
                "cost": service.get("cost", 0),
                "region": service.get("region"),
                "description": service.get("description"),
                "tags": service.get("tags")
            }
            services_summary.append(service_info)
            total_cost += service.get("cost", 0)
        
        # Clear any proxy environment variables that might interfere
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
        for var in proxy_vars:
            if var in os.environ:
                del os.environ[var]
        
        # Prepare the prompt
        prompt = f"""
        As a cloud cost optimization expert, analyze the following organization's cloud infrastructure and services:
        
        Organization: {org_data.get("name")}
        Budget: ${org_data.get("budget", "Not set")} per month
        Total Current Cost: ${total_cost:.2f} per month
        
        Services:
        {json.dumps(services_summary, indent=2)}
        
        Please provide:
        1. Cost Optimization Recommendations (specific suggestions to reduce costs)
        2. Security Analysis (potential security improvements)
        3. Performance Optimization (suggestions to improve performance)
        4. Budget Analysis (how they're performing against budget)
        5. Architecture Recommendations (best practices and improvements)
        6. Risk Assessment (potential risks and mitigation strategies)
        
        Format the response as a comprehensive analysis with actionable insights.
        """
        
        # Call OpenAI API using direct HTTP request
        headers = {
            "Authorization": f"Bearer {api_key_data['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a cloud infrastructure and cost optimization expert. Provide detailed, actionable insights about cloud services and spending."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        print("Making OpenAI API request...")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"OpenAI API error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"OpenAI API error: {response.text}"
            )
        
        response_data = response.json()
        insights = response_data['choices'][0]['message']['content']
        print("Successfully generated AI insights")
        
        # Store insights for caching (optional)
        insights_key = f"insights:{org_id}:{current_user.id}"
        redis_db.set(insights_key, {
            "insights": insights,
            "generated_at": datetime.utcnow().isoformat(),
            "total_cost": total_cost,
            "services_count": len(services)
        }, ex=3600)  # Cache for 1 hour
        
        return {
            "insights": insights,
            "total_cost": total_cost,
            "services_count": len(services),
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except requests.RequestException as e:
        print(f"Request error: {e}")
        raise HTTPException(status_code=400, detail=f"OpenAI API request error: {str(e)}")
    except Exception as e:
        print(f"General error: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")

@router.get("/{org_id}/members")
async def get_organization_members(
    org_id: str,
    current_user: User = Depends(get_current_user)
):
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Get member details
    members = []
    for member_id in org_data["members"]:
        user_key = f"user:{member_id}"
        user_data = redis_db.get(user_key)
        if user_data:
            members.append({
                "id": member_id,
                "email": user_data["email"],
                "is_owner": member_id == org_data["owner_id"]
            })
    
    return {"members": members}

# Helper functions for permission checking
def is_owner(org_data: dict, user_id: str) -> bool:
    """Check if user is the owner of the organization"""
    return org_data["owner_id"] == user_id

def is_moderator(org_data: dict, user_id: str) -> bool:
    """Check if user is a moderator of the organization"""
    return user_id in org_data.get("moderators", [])

def has_moderator_access(org_data: dict, user_id: str) -> bool:
    """Check if user has moderator access (owner or moderator)"""
    # Ensure backwards compatibility
    if "moderators" not in org_data:
        org_data["moderators"] = []
    return is_owner(org_data, user_id) or is_moderator(org_data, user_id)

# Moderator Management Endpoints
@router.post("/{org_id}/moderators")
async def add_moderator_to_organization(
    org_id: str,
    moderator_data: AddModeratorToOrg,
    current_user: User = Depends(get_current_user)
):
    """Add a moderator to the organization (owner only)"""
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if not is_owner(org_data, current_user.id):
        raise HTTPException(status_code=403, detail="Only organization owner can add moderators")
    
    # Find user by email
    email_key = f"email:{moderator_data.user_email}"
    user_id = redis_db.get(email_key)
    
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user is a member of the organization
    if user_id not in org_data["members"]:
        raise HTTPException(status_code=400, detail="User must be a member before becoming a moderator")
    
    # Check if user is already a moderator
    if user_id in org_data.get("moderators", []):
        raise HTTPException(status_code=400, detail="User is already a moderator")
    
    # Can't make owner a moderator (they already have all permissions)
    if user_id == org_data["owner_id"]:
        raise HTTPException(status_code=400, detail="Owner already has all permissions")
    
    # Add user as moderator
    if "moderators" not in org_data:
        org_data["moderators"] = []
    
    org_data["moderators"].append(user_id)
    redis_db.set(org_key, org_data)
    
    return {"message": "User added as moderator successfully"}

@router.delete("/{org_id}/moderators/{user_id}")
async def remove_moderator_from_organization(
    org_id: str,
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """Remove a moderator from the organization (owner only)"""
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if not is_owner(org_data, current_user.id):
        raise HTTPException(status_code=403, detail="Only organization owner can remove moderators")
    
    # Remove user from moderators
    if user_id in org_data.get("moderators", []):
        org_data["moderators"].remove(user_id)
        redis_db.set(org_key, org_data)
        return {"message": "Moderator removed successfully"}
    else:
        raise HTTPException(status_code=400, detail="User is not a moderator")

@router.get("/{org_id}/moderators")
async def get_organization_moderators(
    org_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get list of organization moderators"""
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Get moderator details
    moderators = []
    for moderator_id in org_data.get("moderators", []):
        user_key = f"user:{moderator_id}"
        user_data = redis_db.get(user_key)
        if user_data:
            moderators.append({
                "id": moderator_id,
                "email": user_data["email"]
            })
    
    return {"moderators": moderators}

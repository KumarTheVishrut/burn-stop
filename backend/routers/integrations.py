from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from datetime import datetime

from models.integration import (
    Integration, IntegrationCreate, IntegrationUpdate, 
    TestIntegrationRequest, IntegrationType
)
from models.user import User
from routers.auth import get_current_user
from utils.redis_db import redis_db
from utils.integrations import IntegrationService

router = APIRouter(prefix="/integrations", tags=["integrations"])

@router.post("/", response_model=Integration)
async def create_integration(
    integration: IntegrationCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new integration for an organization"""
    # Check if user has access to this organization
    if integration.organization_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if current user is owner of the organization
    org_key = f"org:{integration.organization_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if org_data["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only organization owner can manage integrations")
    
    # Check if integration type already exists for this organization
    existing_key = f"integration:{integration.organization_id}:{integration.type.value}"
    if redis_db.get(existing_key):
        raise HTTPException(status_code=400, detail=f"{integration.type.value} integration already exists for this organization")
    
    # Create integration
    integration_id = str(uuid.uuid4())
    integration_data = {
        "id": integration_id,
        "organization_id": integration.organization_id,
        "type": integration.type.value,
        "config": integration.config,
        "enabled": True,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    # Save integration
    redis_db.set(existing_key, integration_data)
    
    return Integration(**integration_data)

@router.get("/organizations/{org_id}", response_model=List[Integration])
async def list_integrations(
    org_id: str,
    current_user: User = Depends(get_current_user)
):
    """List all integrations for an organization"""
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if org_data["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only organization owner can view integrations")
    
    integrations = []
    
    # Search for all integration types for this organization
    for integration_type in IntegrationType:
        integration_key = f"integration:{org_id}:{integration_type.value}"
        integration_data = redis_db.get(integration_key)
        if integration_data:
            integrations.append(Integration(**integration_data))
    
    return integrations

@router.get("/organizations/{org_id}/types/{integration_type}", response_model=Integration)
async def get_integration(
    org_id: str,
    integration_type: IntegrationType,
    current_user: User = Depends(get_current_user)
):
    """Get a specific integration by type"""
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if org_data["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only organization owner can view integrations")
    
    integration_key = f"integration:{org_id}:{integration_type.value}"
    integration_data = redis_db.get(integration_key)
    
    if not integration_data:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    return Integration(**integration_data)

@router.put("/organizations/{org_id}/types/{integration_type}", response_model=Integration)
async def update_integration(
    org_id: str,
    integration_type: IntegrationType,
    update_data: IntegrationUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update an existing integration"""
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if org_data["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only organization owner can manage integrations")
    
    integration_key = f"integration:{org_id}:{integration_type.value}"
    integration_data = redis_db.get(integration_key)
    
    if not integration_data:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    # Update fields
    if update_data.config is not None:
        integration_data["config"] = update_data.config
    if update_data.enabled is not None:
        integration_data["enabled"] = update_data.enabled
    
    integration_data["updated_at"] = datetime.utcnow().isoformat()
    
    # Save updated integration
    redis_db.set(integration_key, integration_data)
    
    return Integration(**integration_data)

@router.delete("/organizations/{org_id}/types/{integration_type}")
async def delete_integration(
    org_id: str,
    integration_type: IntegrationType,
    current_user: User = Depends(get_current_user)
):
    """Delete an integration"""
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if org_data["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only organization owner can manage integrations")
    
    integration_key = f"integration:{org_id}:{integration_type.value}"
    integration_data = redis_db.get(integration_key)
    
    if not integration_data:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    # Delete integration
    redis_db.delete(integration_key)
    
    return {"message": "Integration deleted successfully"}

@router.post("/organizations/{org_id}/types/{integration_type}/test")
async def test_integration(
    org_id: str,
    integration_type: IntegrationType,
    test_request: TestIntegrationRequest,
    current_user: User = Depends(get_current_user)
):
    """Test an integration by sending a test message"""
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if org_data["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only organization owner can test integrations")
    
    integration_key = f"integration:{org_id}:{integration_type.value}"
    integration_data = redis_db.get(integration_key)
    
    if not integration_data:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    if not integration_data["enabled"]:
        raise HTTPException(status_code=400, detail="Integration is disabled")
    
    # Send test message
    success = await IntegrationService.send_alert_to_integration(
        integration_type=integration_type.value,
        config=integration_data["config"],
        message=test_request.message,
        subject="🔥 BurnStop Test Alert"
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to send test message")
    
    return {"message": "Test message sent successfully"}

@router.post("/organizations/{org_id}/send-alert")
async def send_alert_to_all_integrations(
    org_id: str,
    alert_message: str,
    current_user: User = Depends(get_current_user)
):
    """Send an alert to all enabled integrations for an organization"""
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if org_data["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only organization owner can send alerts")
    
    results = []
    
    # Send to all enabled integrations
    for integration_type in IntegrationType:
        integration_key = f"integration:{org_id}:{integration_type.value}"
        integration_data = redis_db.get(integration_key)
        
        if integration_data and integration_data["enabled"]:
            success = await IntegrationService.send_alert_to_integration(
                integration_type=integration_type.value,
                config=integration_data["config"],
                message=alert_message,
                subject="🔥 BurnStop Alert"
            )
            
            results.append({
                "type": integration_type.value,
                "success": success
            })
    
    return {
        "message": "Alerts sent to all enabled integrations",
        "results": results
    }

@router.get("/test-configurations")
async def get_test_configurations():
    """Get test integration configurations for demonstration"""
    return {
        "slack": {
            "webhook_url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
            "channel": "#test-alerts",
            "username": "BurnStop-Test",
            "description": "Test Slack webhook for demonstration"
        },
        "google_workspace": {
            "webhook_url": "https://chat.googleapis.com/v1/spaces/AAAA_SAMPLE_SPACE/messages?key=SAMPLE_KEY",
            "space_name": "BurnStop Test Space",
            "description": "Test Google Chat webhook for demonstration"
        },
        "discord": {
            "webhook_url": "https://discord.com/api/webhooks/000000000000000000/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "username": "BurnStop-Test",
            "description": "Test Discord webhook for demonstration"
        },
        "teams": {
            "webhook_url": "https://outlook.office.com/webhook/test-webhook-url",
            "description": "Test Microsoft Teams webhook for demonstration"
        },
        "email": {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "email": "test@burnstop.dev",
            "app_password": "test-app-password",
            "to_email": "admin@burnstop.dev",
            "from_name": "BurnStop Test Alerts",
            "description": "Test email configuration for demonstration"
        }
    }

@router.post("/organizations/{org_id}/test-all-types")
async def test_all_integration_types(
    org_id: str,
    current_user: User = Depends(get_current_user)
):
    """Test all integration types with sample configurations"""
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if org_data["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only organization owner can test integrations")
    
    test_message = "🔥 This is a test alert from BurnStop! All integration types are working correctly."
    results = []
    
    for integration_type in IntegrationType:
        try:
            test_config = IntegrationService.get_test_integration_config(integration_type.value)
            if test_config:
                success = await IntegrationService.send_alert_to_integration(
                    integration_type=integration_type.value,
                    config=test_config,
                    message=test_message,
                    subject="🔥 BurnStop Test Alert"
                )
                
                results.append({
                    "type": integration_type.value,
                    "success": success,
                    "config": test_config,
                    "message": "Test completed successfully" if success else "Test failed"
                })
            else:
                results.append({
                    "type": integration_type.value,
                    "success": False,
                    "message": "No test configuration available"
                })
                
        except Exception as e:
            results.append({
                "type": integration_type.value,
                "success": False,
                "message": f"Test failed: {str(e)}"
            })
    
    return {
        "message": "All integration types tested",
        "test_message": test_message,
        "results": results
    }

@router.post("/organizations/{org_id}/setup-test-integrations")
async def setup_test_integrations(
    org_id: str,
    current_user: User = Depends(get_current_user)
):
    """Setup test integrations for an organization"""
    # Check if user has access to this organization
    if org_id not in current_user.organizations:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if current user is owner of the organization
    org_key = f"org:{org_id}"
    org_data = redis_db.get(org_key)
    
    if not org_data:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if org_data["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only organization owner can setup integrations")
    
    results = []
    
    for integration_type in IntegrationType:
        try:
            # Check if integration already exists
            existing_key = f"integration:{org_id}:{integration_type.value}"
            if redis_db.get(existing_key):
                results.append({
                    "type": integration_type.value,
                    "success": False,
                    "message": "Integration already exists"
                })
                continue
            
            # Get test configuration
            test_config = IntegrationService.get_test_integration_config(integration_type.value)
            if not test_config:
                results.append({
                    "type": integration_type.value,
                    "success": False,
                    "message": "No test configuration available"
                })
                continue
            
            # Create test integration
            integration_id = str(uuid.uuid4())
            integration_data = {
                "id": integration_id,
                "organization_id": org_id,
                "type": integration_type.value,
                "config": test_config,
                "enabled": True,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "is_test": True  # Mark as test integration
            }
            
            # Save integration
            redis_db.set(existing_key, integration_data)
            
            results.append({
                "type": integration_type.value,
                "success": True,
                "message": "Test integration created successfully",
                "config": test_config
            })
            
        except Exception as e:
            results.append({
                "type": integration_type.value,
                "success": False,
                "message": f"Failed to create test integration: {str(e)}"
            })
    
    return {
        "message": "Test integrations setup completed",
        "results": results
    } 
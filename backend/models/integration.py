from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from enum import Enum

class IntegrationType(str, Enum):
    SLACK = "slack"
    GOOGLE_WORKSPACE = "google_workspace"
    EMAIL = "email"
    DISCORD = "discord"
    TEAMS = "teams"

class SlackIntegration(BaseModel):
    webhook_url: str
    channel: Optional[str] = None
    username: Optional[str] = "BurnStop"
    enabled: bool = True

class GoogleWorkspaceIntegration(BaseModel):
    webhook_url: str
    space_name: Optional[str] = None
    enabled: bool = True

class EmailIntegration(BaseModel):
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    email: EmailStr
    app_password: str  # Gmail app password or SMTP password
    from_name: Optional[str] = "BurnStop Alerts"
    enabled: bool = True

class DiscordIntegration(BaseModel):
    webhook_url: str
    username: Optional[str] = "BurnStop"
    enabled: bool = True

class TeamsIntegration(BaseModel):
    webhook_url: str
    enabled: bool = True

class IntegrationCreate(BaseModel):
    organization_id: str
    type: IntegrationType
    config: Dict[str, Any]

class IntegrationUpdate(BaseModel):
    config: Optional[Dict[str, Any]] = None
    enabled: Optional[bool] = None

class Integration(BaseModel):
    id: str
    organization_id: str
    type: IntegrationType
    config: Dict[str, Any]
    enabled: bool
    created_at: str
    updated_at: str

class TestIntegrationRequest(BaseModel):
    message: str = "🔥 Test alert from BurnStop! Your integration is working correctly." 
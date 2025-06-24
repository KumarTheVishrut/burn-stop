from pydantic import BaseModel
from typing import Optional
from enum import Enum
import uuid
from datetime import datetime

class CloudPlatform(str, Enum):
    aws = "aws"
    gcp = "gcp"
    azure = "azure"
    other = "other"

class ServiceType(str, Enum):
    # AWS Services
    ec2 = "ec2"
    s3 = "s3"
    rds = "rds"
    lambda_aws = "lambda"
    eks = "eks"
    ecs = "ecs"
    cloudfront = "cloudfront"
    route53 = "route53"
    vpc = "vpc"
    
    # GCP Services
    compute_engine = "compute_engine"
    cloud_storage = "cloud_storage"
    cloud_sql = "cloud_sql"
    cloud_functions = "cloud_functions"
    gke = "gke"
    cloud_run = "cloud_run"
    bigquery = "bigquery"
    vertex_ai = "vertex_ai"
    
    # Azure Services
    virtual_machines = "virtual_machines"
    blob_storage = "blob_storage"
    sql_database = "sql_database"
    azure_functions = "azure_functions"
    aks = "aks"
    container_instances = "container_instances"
    cosmos_db = "cosmos_db"
    cognitive_services = "cognitive_services"
    
    # Instance Types
    t3_micro = "t3_micro"
    t3_small = "t3_small"
    t3_medium = "t3_medium"
    t3_large = "t3_large"
    m5_large = "m5_large"
    c5_large = "c5_large"
    r5_large = "r5_large"
    g4dn_xlarge = "g4dn_xlarge"
    p3_2xlarge = "p3_2xlarge"
    
    # GCP Instance Types
    n1_standard_1 = "n1_standard_1"
    n1_standard_2 = "n1_standard_2"
    n1_standard_4 = "n1_standard_4"
    n2_standard_2 = "n2_standard_2"
    c2_standard_4 = "c2_standard_4"
    
    # General Categories
    cloud = "cloud"
    infra = "infra"
    subscription = "subscription"
    api = "api"
    database = "database"
    storage = "storage"
    networking = "networking"
    security = "security"
    monitoring = "monitoring"
    analytics = "analytics"

class ServiceStatus(str, Enum):
    active = "active"
    pending_deletion = "pending_deletion"
    suspended = "suspended"
    terminated = "terminated"

class ServiceBase(BaseModel):
    name: str
    platform: CloudPlatform
    service_type: ServiceType
    cost: float
    reminder_date: str  # ISO date string
    
    # Infrastructure tracking
    iam_number: Optional[str] = None
    instance_id: Optional[str] = None
    service_id: Optional[str] = None
    region: Optional[str] = None
    
    # API specific
    api_quota_tokens: Optional[int] = None
    api_usage_tokens: Optional[int] = None
    
    # Additional metadata
    description: Optional[str] = None
    tags: Optional[str] = None  # JSON string of tags
    owner_email: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: str
    org_id: str
    status: ServiceStatus = ServiceStatus.active
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    platform: Optional[CloudPlatform] = None
    service_type: Optional[ServiceType] = None
    cost: Optional[float] = None
    reminder_date: Optional[str] = None
    status: Optional[ServiceStatus] = None
    
    # Infrastructure tracking
    iam_number: Optional[str] = None
    instance_id: Optional[str] = None
    service_id: Optional[str] = None
    region: Optional[str] = None
    
    # API specific
    api_quota_tokens: Optional[int] = None
    api_usage_tokens: Optional[int] = None
    
    # Additional metadata
    description: Optional[str] = None
    tags: Optional[str] = None
    owner_email: Optional[str] = None

class Reminder(BaseModel):
    id: str
    service_id: str
    service_name: str
    cost: float
    reminder_date: str
    org_id: str

class ReminderAcknowledge(BaseModel):
    action_taken: str  # Description of what action was taken

class ServiceAnalytics(BaseModel):
    total_monthly_cost: float
    total_services: int
    cost_by_platform: dict
    cost_by_type: dict
    predicted_next_month: float
    cost_trend: list  # Historical cost data for predictions

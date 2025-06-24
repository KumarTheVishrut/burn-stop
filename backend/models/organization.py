from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str
    budget: Optional[float] = None  # Monthly budget in dollars

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: str
    owner_id: str
    members: List[str] = []
    created_at: str

    class Config:
        from_attributes = True

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None

class AddUserToOrg(BaseModel):
    user_email: str

class UpdateOrganizationBudget(BaseModel):
    budget: float

import uuid
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class CompanyBase(BaseModel):
    name: str
    website: Optional[str] = None
    industry: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class JobRoleBase(BaseModel):
    company_id: uuid.UUID
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    level: Optional[str] = None


class JobRoleCreate(JobRoleBase):
    pass


class JobRoleRead(JobRoleBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class ApplicationBase(BaseModel):
    company_id: uuid.UUID
    role_id: uuid.UUID
    status: Optional[str] = 'applied'  # applied, screening, assessment, interview, offered, rejected
    applied_at: Optional[datetime] = None
    app_metadata: Optional[dict] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationRead(ApplicationBase):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

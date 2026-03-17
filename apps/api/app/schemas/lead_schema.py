from pydantic import BaseModel

class LeadCreate(BaseModel):
    campaign_id: str
    first_name: str
    last_name: str
    email: str
    company: str
    job_title: str

class LeadResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    company: str
    job_title: str

    class Config:
        from_attributes = True
from pydantic import BaseModel
from typing import List

class CampaignCreate(BaseModel):
    campaign_name: str
    product_name: str
    product_description: str
    goal: str
    lead_sources: List[str]
    lead_limit: int

class CampaignResponse(BaseModel):
    id: str
    campaign_name: str
    product_name: str
    goal: str
    lead_sources: List[str]
    lead_limit: int

    class Config:
        from_attributes = True
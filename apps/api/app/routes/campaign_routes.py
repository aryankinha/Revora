from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.campaign import Campaign
from app.schemas.campaign_schema import CampaignCreate

router = APIRouter(prefix="/campaign", tags=["Campaign"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_campaign(data: CampaignCreate, db: Session = Depends(get_db)):

    campaign = Campaign(
        campaign_name=data.campaign_name,
        product_name=data.product_name,
        product_description=data.product_description,
        goal=data.goal,
        lead_sources=data.lead_sources,
        lead_limit=data.lead_limit
    )

    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    return {
        "message": "Campaign created",
        "campaign_id": campaign.id
    }


@router.get("/")
def get_campaigns(db: Session = Depends(get_db)):

    campaigns = db.query(Campaign).all()

    return campaigns
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.campaign import Campaign
from app.models.icp_filter import ICP
from app.models.leads import Leads as Lead

from app.services.apollo_lead_generator import generate_leads_from_apollo
from app.services.linkedin_lead_generator import generate_leads_from_linkedin

router = APIRouter(prefix="/campaign", tags=["Leads"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def process_leads_background(campaign_id: str, icp_id: str):
    db = SessionLocal()
    try:
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        icp = db.query(ICP).filter(ICP.id == icp_id).first()

        if not campaign or not icp:
            return

        leads = []
        
        if "Apollo" in campaign.lead_sources or not campaign.lead_sources:
            leads.extend(generate_leads_from_apollo(icp, campaign.lead_limit))
            
        if "LinkedIn" in campaign.lead_sources:
            leads.extend(generate_leads_from_linkedin(icp, campaign.lead_limit))

        for lead in leads:
            new_lead = Lead(
                campaign_id=campaign_id,
                first_name=lead["first_name"],
                last_name=lead["last_name"],
                email=lead["email"],
                company=lead["company"],
                job_title=lead["job_title"],
                linkedin=lead["linkedin"]
            )
            db.add(new_lead)
        
        db.commit()
    except Exception as e:
        print(f"Error generating leads: {e}")
        db.rollback()
    finally:
        db.close()


@router.post("/{campaign_id}/generate-leads")
def generate_leads(campaign_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    # Fetch campaign
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        return {"error": "Campaign not found"}

    # Fetch ICP
    icp = db.query(ICP).filter(ICP.campaign_id == campaign_id).first()

    if not icp:
        return {"error": "ICP not found"}

    background_tasks.add_task(process_leads_background, campaign_id, icp.id)

    return {
        "message": "Leads generation started in the background",
        "status": "processing"
    }


@router.get("/{campaign_id}")
def get_leads(campaign_id: str, db: Session = Depends(get_db)):
    leads = db.query(Lead).filter(Lead.campaign_id == campaign_id).all()
    return leads
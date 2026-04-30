import base64
from email.message import EmailMessage
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from pydantic import BaseModel

from app.db.database import SessionLocal
from app.models.user import User
from app.models.leads import Leads
from app.models.campaign import Campaign
from app.models.icp_filter import ICP
from app.services.email_generator import EmailGenerator
from app.core.config import settings
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/gmail", tags=["Gmail Integration"])

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/auth")
def gmail_auth():
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(
            status_code=500, detail="Google Client credentials not configured in .env"
        )

    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "project_id": "revora-demo",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
        }
    }

    flow = Flow.from_client_config(
        client_config, scopes=SCOPES, redirect_uri=settings.GOOGLE_REDIRECT_URI
    )

    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    return RedirectResponse(auth_url)


@router.get("/callback")
def gmail_callback(
    request: Request,
    code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "project_id": "revora-demo",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
        }
    }

    flow = Flow.from_client_config(
        client_config, scopes=SCOPES, redirect_uri=settings.GOOGLE_REDIRECT_URI
    )

    try:
        flow.fetch_token(code=code)
        credentials = flow.credentials

        current_user.google_access_token = credentials.token
        current_user.google_refresh_token = credentials.refresh_token
        current_user.token_expiry = credentials.expiry.isoformat() if credentials.expiry else None
        current_user.connected_email = (
            "connected-via-oauth@gmail.com"  # Mocked, needs additional scope to fetch actual email
        )

        db.commit()
        return RedirectResponse(f"{settings.FRONTEND_URL}/dashboard/leads?gmail_connected=true")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth Flow Failed: {e}")


class CampaignEmailPayload(BaseModel):
    subject: str
    html_body: str


class PersonalizedCampaignEmailPayload(BaseModel):
    goal: str = ""
    tone: str = "Professional"
    value_props: str = ""
    subject_format: str = ""
    sender_name: str = ""


def _campaign_sender_name(campaign: Campaign, current_user: User) -> str:
    company_name = (campaign.product_name or current_user.company_name or "").strip()
    return f"{company_name} Team" if company_name else "Revora Team"


def _lead_full_name(lead: Leads) -> str:
    return f"{lead.first_name or ''} {lead.last_name or ''}".strip() or "there"


def _merge_template(value: str, lead: Leads) -> str:
    replacements = {
        "{{name}}": _lead_full_name(lead),
        "{{first_name}}": lead.first_name or _lead_full_name(lead),
        "{{last_name}}": lead.last_name or "",
        "{{company}}": lead.company or "",
        "{{company_name}}": lead.company or "",
        "{{job_title}}": lead.job_title or "",
        "{{email}}": lead.email or "",
    }
    merged = value or ""
    for key, replacement in replacements.items():
        merged = merged.replace(key, replacement)
    return merged


def _get_gmail_service(current_user: User):
    if not current_user.google_access_token:
        raise HTTPException(
            status_code=400, detail="Gmail not connected. Please authenticate first."
        )

    credentials = Credentials(
        token=current_user.google_access_token,
        refresh_token=current_user.google_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=SCOPES,
    )
    return build("gmail", "v1", credentials=credentials)


def _send_email(service, to_email: str, subject: str, html_body: str):
    message = EmailMessage()
    message.set_content(html_body, subtype="html")
    message["To"] = to_email
    message["Subject"] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": encoded_message}).execute()


@router.post("/send-campaign/{campaign_id}")
def send_campaign_emails(
    campaign_id: str,
    payload: CampaignEmailPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = _get_gmail_service(current_user)

    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.user_id == str(current_user.id))
        .first()
    )
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    leads = db.query(Leads).filter(Leads.campaign_id == campaign_id).all()
    if not leads:
        raise HTTPException(status_code=404, detail="No leads found for this campaign")

    sent_count = 0
    errors = []

    for lead in leads:
        try:
            merged_body = _merge_template(payload.html_body, lead)
            merged_subject = _merge_template(payload.subject, lead)
            _send_email(service, lead.email, merged_subject, merged_body)
            sent_count += 1
        except Exception as e:
            errors.append({"lead": lead.email, "error": str(e)})

    return {"sent": sent_count, "errors": errors, "total": len(leads)}


@router.post("/send-personalized-campaign/{campaign_id}")
def send_personalized_campaign_emails(
    campaign_id: str,
    payload: PersonalizedCampaignEmailPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = _get_gmail_service(current_user)

    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.user_id == str(current_user.id))
        .first()
    )
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    leads = db.query(Leads).filter(Leads.campaign_id == campaign_id).all()
    if not leads:
        raise HTTPException(status_code=404, detail="No leads found for this campaign")

    icp = db.query(ICP).filter(ICP.campaign_id == campaign_id).first()
    campaign_info = {
        "product_name": campaign.product_name,
        "product_description": campaign.product_description,
        "goal": campaign.goal,
    }
    icp_info = {"industry": icp.industry, "job_titles": icp.job_titles} if icp else None
    email_gen = EmailGenerator()
    sender_name = payload.sender_name.strip() or _campaign_sender_name(campaign, current_user)

    sent_count = 0
    errors = []
    sent = []

    for lead in leads:
        try:
            lead_info = {
                "first_name": lead.first_name,
                "company": lead.company,
                "job_title": lead.job_title,
            }
            draft = email_gen.generate_personalized_email(
                campaign_info=campaign_info,
                icp_info=icp_info,
                lead_info=lead_info,
                tone=payload.tone,
                goal=payload.goal,
                value_props=payload.value_props,
                subject_format=payload.subject_format,
                sender_name=sender_name,
            )
            if draft.get("error"):
                raise RuntimeError(draft["error"])

            html_body = _merge_template(draft["body"], lead).replace("\n", "<br>")
            subject = _merge_template(draft["subject"], lead)
            _send_email(service, lead.email, subject, html_body)
            sent_count += 1
            sent.append({"lead": lead.email, "subject": subject})
        except Exception as e:
            errors.append({"lead": lead.email, "error": str(e)})

    return {"sent": sent_count, "errors": errors, "total": len(leads), "recipients": sent}

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import requests
import json
import urllib.parse
import time
import uuid

from app.schemas.auth_schema import SignupSchema, LoginSchema
from pydantic import BaseModel
from app.db.database import SessionLocal
from app.models.user import User
from app.core.dependencies import get_current_user
from app.services.auth_service import signup_user, login_user
from app.core.config import settings
from app.core.security import create_access_token
from app.core.hashing import hash_password
from app.utils.seed_utils import seed_welcome_data

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup")
def signup(data: SignupSchema, db: Session = Depends(get_db)):
    return signup_user(db, data)


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    return login_user(db, data)


@router.get("/google/login")
def google_sso_login():
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google Client credentials missing")

    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={urllib.parse.quote(settings.GOOGLE_SSO_REDIRECT_URI)}&"
        "response_type=code&"
        "scope=openid%20profile%20email%20https://www.googleapis.com/auth/gmail.send&"
        "access_type=offline&"
        "prompt=consent"
    )
    return RedirectResponse(auth_url)


@router.get("/google/callback")
def google_sso_callback(request: Request, code: str, db: Session = Depends(get_db)):
    try:
        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_SSO_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        res = requests.post("https://oauth2.googleapis.com/token", data=token_data)
        token_json = res.json()

        if "access_token" not in token_json:
            print("Token error:", token_json)
            raise Exception("No access token provided by Google")

        access_token_google = token_json["access_token"]

        user_info_response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token_google}"},
        )
        user_info = user_info_response.json()

        email = user_info.get("email")
        name = user_info.get("name", "Google User")

        if not email:
            raise HTTPException(status_code=400, detail="Could not retrieve email.")

        user = db.query(User).filter(User.email == email).first()

        if not user:
            random_pwd = hash_password(str(uuid.uuid4()))
            user = User(
                full_name=name,
                email=email,
                password=random_pwd,
                role="founder",
                company_name=None,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            seed_welcome_data(db, str(user.id), user.email)

        # Always update Google tokens so Gmail connection stays active
        user.google_access_token = access_token_google
        if "refresh_token" in token_json:
            user.google_refresh_token = token_json["refresh_token"]

        user.token_expiry = str(int(time.time()) + token_json.get("expires_in", 3599))
        user.connected_email = email
        db.commit()

        access_token = create_access_token({"user_id": str(user.id)})

        user_data = {
            "id": str(user.id),
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "company_name": user.company_name,
        }
        user_data_str = urllib.parse.quote(json.dumps(user_data))

        return RedirectResponse(
            f"{settings.FRONTEND_URL}/dashboard?token={access_token}&user={user_data_str}"
        )

    except Exception as e:
        print(f"SSO Error: {e}")
        return RedirectResponse(f"{settings.FRONTEND_URL}/auth/login?error=Google_SSO_Failed")


class OnboardingUpdate(BaseModel):
    company_name: str
    role: str


@router.post("/onboarding")
def complete_onboarding(
    data: OnboardingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == current_user.id).first()
    user.company_name = data.company_name
    user.role = data.role
    db.commit()
    return {"message": "Onboarding complete", "company_name": user.company_name, "role": user.role}

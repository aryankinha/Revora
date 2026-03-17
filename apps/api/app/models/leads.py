import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class Leads(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String)

    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    company = Column(String)
    job_title = Column(String)
    linkedin = Column(String)
from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base
from app.routes.auth_routes import router as auth_router
from app.routes.dashboard_routes import router as dashboard_router
from app.models import user
from app.routes import campaign_routes
from app.routes import icp_routes
from app.routes import lead_routes

app = FastAPI(title="Revora API")


Base.metadata.create_all(bind=engine)


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(campaign_routes.router)
app.include_router(icp_routes.router)
app.include_router(lead_routes.router)

@app.get("/")
def root():
    return {"message": "Revora API Running"}
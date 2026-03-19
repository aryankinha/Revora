from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
from app.db.base import Base
from app.routes.auth_routes import router as auth_router
from app.routes.dashboard_routes import router as dashboard_router
from app.models import user

app = FastAPI(title="Revora API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])


@app.get("/")
def root():
    return {"message": "Revora API Running"}
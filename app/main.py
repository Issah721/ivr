from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.config.settings import settings
from app.routers import admin, voice, dashboard
from contextlib import asynccontextmanager
from app.services.scheduler import start_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield

app = FastAPI(
    title="IVR Medication Adherence System",
    description="MVP for automated outward calls and DTMF adherence tracking",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("app/static/audio", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(admin.router)
app.include_router(voice.router)
app.include_router(dashboard.router)
@app.get("/health", tags=["system"])
def health_check():
    return {
        "status": "up",
        "environment": settings.app_env,
        "database": "configured" if settings.database_url else "missing",
    }

# App initialization logs and standard run block
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

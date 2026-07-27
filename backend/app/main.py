from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dashboard.dashboard_api import router as dashboard_router
from app.dashboard.route_api import router as route_router
from app.dashboard.simulation_api import router as simulation_router
from app.dashboard.status_api import router as status_router


app = FastAPI(
    title="Dynamic Fire Evacuation System",
    version="1.0"
)


# ==============================
# CORS Configuration
# Allows React frontend to access FastAPI backend
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# API Routers
# ==============================

app.include_router(dashboard_router)
app.include_router(route_router)
app.include_router(simulation_router)
app.include_router(status_router)


# ==============================
# Basic System Endpoints
# ==============================

@app.get("/")
def home():

    return {

        "system": "Dynamic Fire Evacuation System",

        "status": "running"

    }



@app.get("/health")
def health():

    return {

        "status": "ONLINE",

        "service": "Dynamic Fire Evacuation System"

    }
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.seed import seed_database
from app.routers import pathways, beyonders, potions, commissions, claims


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield


app = FastAPI(
    title="Lord of the Mysteries - Tarot Administrative API",
    description="Administrative backend API for managing Beyonder Operatives, Potion Codex, Commissions, and Mission Claims.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS Middleware as requested in spec
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(pathways.router)
app.include_router(beyonders.router)
app.include_router(potions.router)
app.include_router(commissions.router)
app.include_router(claims.router)


@app.get("/")
def root():
    return {
        "status": "online",
        "system": "Lord of the Mysteries Tarot Command Center API",
        "documentation": "/docs"
    }

import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import (
    worker, position, sub_position,
    shift, supplier, item,
    problem_comment, production_log,
    division, department,
    production_target, attendance
)

app = FastAPI(
    title="MKP Operational API",
    redirect_slashes=False  # Disable automatic redirect from /positions to /positions/
)

# Health check endpoint
@app.get("/")
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "MKP Operational API"}

# CORS configuration - supports both development and production
# Set ALLOWED_ORIGINS environment variable for production (comma-separated)
# Development origins are always included
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "").strip()

# Always include common development origins
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5174",
    "http://127.0.0.1:5174"
]

# Add production origins from environment variable if set
if allowed_origins_env:
    production_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
    allowed_origins.extend(production_origins)
    # Remove duplicates while preserving order
    allowed_origins = list(dict.fromkeys(allowed_origins))

# Log allowed origins for debugging
print(f"CORS Allowed Origins: {allowed_origins}")

# Add CORS middleware - MUST be added before routers
# Support Vercel preview deployments with regex pattern
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",  # Allow all Vercel preview deployments
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Create tables (alembic migration is preferred, but this ensures tables exist)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not create tables: {e}")
    print("This is OK if using Alembic migrations")

# Include all routers
app.include_router(division.router)
app.include_router(department.router)
app.include_router(worker.router)
app.include_router(position.router)
app.include_router(sub_position.router)
app.include_router(shift.router)
app.include_router(supplier.router)
app.include_router(item.router)
app.include_router(problem_comment.router)
app.include_router(production_log.router)
app.include_router(production_target.router)
app.include_router(attendance.router)

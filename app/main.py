from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import (
    worker, position, sub_position,
    shift, supplier, item,
    problem_comment, production_log,
    division, department
)

app = FastAPI(title="MKP Operational API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

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

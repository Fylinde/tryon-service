from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import BaseModel, engine
from app.routes import tryon_routes  # Importing your routes
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Initialize database tables
BaseModel.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI(
    title="Try-On Service",
    description="A microservice for enabling virtual try-on functionality.",
    version="1.0.0"
)

# Middleware setup for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tryon_routes.router, prefix="/api/v1/tryon", tags=["Try-On"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Try-On Service!"}

@app.on_event("startup")
def startup_event():
    logger.info("Try-On Service is starting...")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Try-On Service is shutting down...")
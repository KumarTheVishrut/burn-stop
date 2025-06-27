from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from routers import auth, organizations, services, reminders, integrations

app = FastAPI(
    title="BurnStop API",
    description="Stop burning money on subscriptions and cloud infrastructure",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(organizations.router)
app.include_router(services.router)
app.include_router(reminders.router)
app.include_router(integrations.router)

@app.get("/")
async def root():
    return {"message": "BurnStop API - Stop burning money on subscriptions!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

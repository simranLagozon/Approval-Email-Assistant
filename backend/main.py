"""
Approval AI Dashboard - FastAPI Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from routers import auth, emails, actions, summary

app = FastAPI(
    title="Approval AI Dashboard API",
    description="Microsoft Outlook + OpenAI powered approval management system",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(emails.router, prefix="/api/emails", tags=["Emails"])
app.include_router(actions.router, prefix="/api/actions", tags=["Actions"])
app.include_router(summary.router, prefix="/api/summary", tags=["AI Summary"])

# ✅ Correct frontend path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # go out of backend/
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# ✅ Serve static files
app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")

# ✅ Serve index.html
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}
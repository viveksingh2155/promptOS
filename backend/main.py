import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, run_migrations
from routers import optimizer, history, templates

# Create all database tables
Base.metadata.create_all(bind=engine)
run_migrations()

app = FastAPI(
    title="PromptOS API",
    description="4-agent AI prompt optimization pipeline",
    version="1.0.0",
)

# Configure CORS origins from environment variable
# Format: Comma-separated list of allowed origins
# Example: "https://promptos.vercel.app,https://www.promptos.com"
cors_origins_str = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
)
cors_origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include endpoint routers
app.include_router(optimizer.router, prefix="/api", tags=["optimize"])
app.include_router(history.router, prefix="/api", tags=["history"])
app.include_router(templates.router, prefix="/api", tags=["templates"])

@app.get("/health")
def health():
    """Health check endpoint for monitoring and load balancers"""
    return {"status": "ok", "version": "1.0.0"}

@app.on_event("startup")
async def startup_event():
    """Verify critical configuration on startup"""
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    print(f"[PromptOS] Starting up...")
    print(f"[PromptOS] Database: {os.getenv('DATABASE_URL', 'sqlite:///./promptos.db')[:50]}...")
    print(f"[PromptOS] CORS Origins: {cors_origins}")
    print(f"[PromptOS] Ollama URL: {ollama_url}")
    print(f"[PromptOS] Ready to optimize prompts!")

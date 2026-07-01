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

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
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
    return {"status": "ok", "version": "1.0.0"}

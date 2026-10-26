import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Support configurable database URL for production (PostgreSQL) or local development (SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./promptos.db")

# Fix for Render/Heroku PostgreSQL URLs (postgres:// -> postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite-specific config
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # Verify connections before using them
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def run_migrations():
    """Run database migrations safely for both SQLite and PostgreSQL"""
    from sqlalchemy import text
    import sqlalchemy.exc
    
    try:
        with engine.begin() as conn:
            # Check if detected_language column exists
            try:
                conn.execute(text("SELECT detected_language FROM prompt_history LIMIT 1"))
            except sqlalchemy.exc.OperationalError:
                try:
                    # PostgreSQL and SQLite compatible ALTER TABLE
                    conn.execute(text("ALTER TABLE prompt_history ADD COLUMN detected_language VARCHAR DEFAULT 'English'"))
                    print("[Migration] Added detected_language column.")
                except Exception as e:
                    print(f"[Migration] detected_language column may already exist: {e}")
            
            # Check if target_language column exists
            try:
                conn.execute(text("SELECT target_language FROM prompt_history LIMIT 1"))
            except sqlalchemy.exc.OperationalError:
                try:
                    conn.execute(text("ALTER TABLE prompt_history ADD COLUMN target_language VARCHAR DEFAULT 'Original'"))
                    print("[Migration] Added target_language column.")
                except Exception as e:
                    print(f"[Migration] target_language column may already exist: {e}")
    except Exception as e:
        print(f"[Migration] Warning: Migration check failed: {e}")
        # Don't fail startup if migrations have issues


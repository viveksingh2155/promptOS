from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./promptos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
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
    from sqlalchemy import text
    with engine.begin() as conn:
        # Check if detected_language column exists
        try:
            conn.execute(text("SELECT detected_language FROM prompt_history LIMIT 1"))
        except Exception:
            try:
                conn.execute(text("ALTER TABLE prompt_history ADD COLUMN detected_language VARCHAR DEFAULT 'English'"))
                print("Migration: Added detected_language column.")
            except Exception as e:
                print("Migration error (detected_language):", e)
        # Check if target_language column exists
        try:
            conn.execute(text("SELECT target_language FROM prompt_history LIMIT 1"))
        except Exception:
            try:
                conn.execute(text("ALTER TABLE prompt_history ADD COLUMN target_language VARCHAR DEFAULT 'Original'"))
                print("Migration: Added target_language column.")
            except Exception as e:
                print("Migration error (target_language):", e)


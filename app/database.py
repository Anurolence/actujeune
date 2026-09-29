import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Vercel's filesystem is read-only except /tmp
if os.path.exists("/var/task"):
    # On Vercel - use /tmp
    DB_PATH = "/tmp/actujeune.db"
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "..", "actujeune.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
print(f"DB URL: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print(f"DB created at {DB_PATH}")
    except Exception as e:
        print(f"DB init error: {e}")
        raise

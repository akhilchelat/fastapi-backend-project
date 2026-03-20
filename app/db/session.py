# how request talk to the db

from sqlalchemy.orm import sessionmaker
from app.db.engine import engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# dependency one session per request, auto close, safe

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

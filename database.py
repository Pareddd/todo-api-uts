from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Kita menggunakan SQLite agar mudah untuk localhost
SQLALCHEMY_DATABASE_URL = "sqlite:///./todolist.db"

# connect_args={"check_same_thread": False} dibutuhkan khusus untuk SQLite di FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency untuk dipanggil di setiap endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
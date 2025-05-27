from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import SYNC_DATABASE_URL

#Движок синхронный для Celery
engine = create_engine(SYNC_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

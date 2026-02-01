from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import MYSQL_URL

engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(bind=engine)

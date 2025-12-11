from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:Vicente5150.@localhost:3306/userdb")

engine = create_engine(
    DATABASE_URL,
    echo=True,  # muestra las consultas SQL en consola
    pool_pre_ping=True  # reconecta si hay desconexión
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
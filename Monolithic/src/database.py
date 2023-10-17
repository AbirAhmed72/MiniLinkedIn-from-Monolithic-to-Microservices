# database.py
from sqlalchemy import create_engine, engine
from sqlalchemy.engine import base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

SQL_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/MiniLinkedIn"

engine = create_engine(SQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

Base =  declarative_base()

def get_db():
    db = SessionLocal()

    # yield db
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)




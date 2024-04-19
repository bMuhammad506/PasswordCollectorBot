from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date,BigInteger ,DateTime 
from datetime import datetime, timedelta
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session

Base = declarative_base()

class Passwords(Base):
    __tablename__ = "passwords"
    site_name = Column(String, primary_key=True)
    site_pass = Column(String, nullable=False)

DATABASE_URL = 'sqlite:///password_record.db'
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
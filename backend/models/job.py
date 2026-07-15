from sqlalchemy import Column, Integer, String, Text,DateTime
from sqlalchemy.sql import func 

from db.database import Base



class StoryJob(Base):
    __tablename__='story_jobs'

    id = Column(Integer, primary_key=True, index=True)
    job_id=Column(String(255),index=True,nullable=False,unique=True)
    session_id=Column(String(255),index=True)
    theme=Column(String)
    story_id=Column(Integer,nullable=True)
    error=Column(String,nullable=True)
    status=Column(String(50),nullable=False,default='pending')
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    completed_at=Column(DateTime(timezone=True),nullable=True)
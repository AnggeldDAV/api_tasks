from db.database import Base
from sqlalchemy import Column, Integer, String, DateTime,Boolean,ForeignKey
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    state= Column(String)
    priority = Column(Boolean)
    date = Column(DateTime)
    user_id = Column(Integer,ForeignKey("users.id"))
    owner = relationship("User",back_populates="tasks")
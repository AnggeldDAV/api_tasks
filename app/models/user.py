from db.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,index=True)
    hashed_password = Column(String)
    tasks = relationship("Task", back_populates="owner")
    

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.time_stamp import TimestampMixin

class Department(Base, TimestampMixin):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True )
    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    employees = relationship("Employee", back_populates="department")
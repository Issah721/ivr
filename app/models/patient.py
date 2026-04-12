from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    name = Column(String)
    language = Column(String, default="English") # English or Swahili
    
    schedules = relationship("MedicationSchedule", back_populates="patient", cascade="all, delete-orphan")
    call_logs = relationship("CallLog", back_populates="patient", cascade="all, delete-orphan")
    reports = relationship("AdherenceReport", back_populates="patient", cascade="all, delete-orphan")

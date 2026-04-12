from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class MedicationSchedule(Base):
    __tablename__ = "medication_schedules"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    time_to_call = Column(String) # e.g., "08:00"
    medication_name = Column(String)
    active = Column(Boolean, default=True)

    patient = relationship("Patient", back_populates="schedules")

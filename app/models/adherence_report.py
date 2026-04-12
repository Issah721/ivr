from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class AdherenceReport(Base):
    __tablename__ = "adherence_reports"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(Date)
    status = Column(String) # taken, not_taken, missed
    
    patient = relationship("Patient", back_populates="reports")

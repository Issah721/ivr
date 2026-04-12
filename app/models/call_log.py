from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    session_id = Column(String, unique=True, index=True) # AT session id
    call_status = Column(String) # queued, ringing, active, completed, failed, etc
    adherence_status = Column(String, nullable=True) # 1=taken, 2=not taken, 3=side effects
    timestamp = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="call_logs")

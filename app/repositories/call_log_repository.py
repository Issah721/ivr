from sqlalchemy.orm import Session
from app.models.call_log import CallLog
from datetime import datetime

class CallLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, patient_id: int, session_id: str, call_status: str):
        log = CallLog(
            patient_id=patient_id,
            session_id=session_id,
            call_status=call_status
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def update_adherence(self, session_id: str, adherence_status: str = None, call_status: str = None):
        log = self.db.query(CallLog).filter(CallLog.session_id == session_id).first()
        if log:
            if adherence_status is not None:
                log.adherence_status = adherence_status
            if call_status is not None:
                log.call_status = call_status
            self.db.commit()
            self.db.refresh(log)
        return log
        
    def get_all(self):
        return self.db.query(CallLog).order_by(CallLog.timestamp.desc()).all()

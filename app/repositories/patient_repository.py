from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.models.medication_schedule import MedicationSchedule

class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_phone(self, phone_number: str):
        return self.db.query(Patient).filter(Patient.phone_number == phone_number).first()

    def get_all(self):
        return self.db.query(Patient).all()
        
    def create(self, patient_data: dict, schedules_data: list = None):
        patient = Patient(
            phone_number=patient_data["phone_number"],
            name=patient_data.get("name"),
            language=patient_data.get("language", "English")
        )
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        
        if schedules_data:
            for s in schedules_data:
                schedule = MedicationSchedule(
                    patient_id=patient.id,
                    time_to_call=s["time_to_call"],
                    medication_name=s["medication_name"],
                    active=s.get("active", True)
                )
                self.db.add(schedule)
            self.db.commit()
        return patient

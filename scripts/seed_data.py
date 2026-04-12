import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.repositories.patient_repository import PatientRepository

def seed():
    db = SessionLocal()
    repo = PatientRepository(db)
    
    patients = [
        {
            "data": {"phone_number": "+254700000001", "name": "John Doe", "language": "English"},
            "schedules": [{"time_to_call": "08:00", "medication_name": "ARV"}]
        },
        {
            "data": {"phone_number": "+254700000002", "name": "Jane Wanjiku", "language": "Swahili"},
            "schedules": [{"time_to_call": "09:00", "medication_name": "Metformin"}]
        },
        {
            "data": {"phone_number": "+254700000003", "name": "Peter Kamau", "language": "Swahili"},
            "schedules": [{"time_to_call": "10:00", "medication_name": "Amlodipine"}]
        }
    ]

    for p in patients:
        existing = repo.get_by_phone(p["data"]["phone_number"])
        if not existing:
            repo.create(p["data"], p["schedules"])
            print(f"Added {p['data']['name']}")
        else:
            print(f"Skipped {p['data']['name']} (already exists)")

    db.close()

if __name__ == "__main__":
    seed()

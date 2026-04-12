import csv
import io
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_api_key
from app.repositories.patient_repository import PatientRepository

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_api_key)]
)

@router.post("/patients/upload")
async def upload_patients_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV allowed.")
    
    content = await file.read()
    decoded = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(decoded))
    
    # Verify exact required headers based on Phase 3 requirements
    # phone, name, language, time_to_call, medication_name
    
    repo = PatientRepository(db)
    success_count = 0
    
    for row in csv_reader:
        phone = row.get("phone")
        if not phone:
            continue
            
        patient_data = {
            "phone_number": phone.strip(),
            "name": row.get("name", "").strip(),
            "language": row.get("language", "English").strip()
        }
        
        schedules_data = []
        if row.get("time_to_call") and row.get("medication_name"):
            schedules_data.append({
                "time_to_call": row.get("time_to_call").strip(),
                "medication_name": row.get("medication_name").strip()
            })
        
        existing = repo.get_by_phone(patient_data["phone_number"])
        if not existing:
            repo.create(patient_data, schedules_data)
            success_count += 1
            
    return {"message": f"Successfully processed {success_count} new patients."}

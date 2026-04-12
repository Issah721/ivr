import csv
import io
from fastapi import APIRouter, Request, Depends, File, UploadFile, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.repositories.patient_repository import PatientRepository
from app.repositories.call_log_repository import CallLogRepository

router = APIRouter(tags=["dashboard"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request, db: Session = Depends(get_db)):
    patient_repo = PatientRepository(db)
    call_log_repo = CallLogRepository(db)
    
    patients = patient_repo.get_all()
    all_logs = call_log_repo.get_all()
    
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    todays_calls = [log for log in all_logs if log.timestamp >= today_start]
    
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "patients": patients,
            "todays_calls": todays_calls,
            "all_logs": all_logs
        }
    )

@router.post("/dashboard/upload-csv", response_class=HTMLResponse)
async def htmx_upload_csv(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        return HTMLResponse("<div class='p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50'>Invalid file format. Only CSV allowed.</div>")
    
    content = await file.read()
    decoded = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(decoded))
    
    repo = PatientRepository(db)
    success_count = 0
    
    for row in csv_reader:
        phone = row.get("phone")
        if not phone: continue
        
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
            
        if not repo.get_by_phone(patient_data["phone_number"]):
            repo.create(patient_data, schedules_data)
            success_count += 1
            
    return HTMLResponse(f"<div class='p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-50'>Successfully processed {success_count} new patients. Please refresh the page to view.</div>")

@router.get("/export/adherence")
async def export_adherence(db: Session = Depends(get_db)):
    call_log_repo = CallLogRepository(db)
    logs = call_log_repo.get_all()
    
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(["ID", "Patient Phone", "Patient Name", "Session ID", "Call Status", "Adherence Status", "Timestamp"])
    
    for log in logs:
        writer.writerow([
            log.id, 
            log.patient.phone_number if log.patient else "N/A",
            log.patient.name if log.patient else "N/A",
            log.session_id,
            log.call_status,
            log.adherence_status,
            log.timestamp.isoformat()
        ])
        
    response = Response(content=stream.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=adherence_report.csv"
    return response

@router.get("/sus", response_class=HTMLResponse)
async def get_sus_form(request: Request):
    return templates.TemplateResponse(request=request, name="sus_questionnaire.html", context={"request": request})

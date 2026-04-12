import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from app.database import SessionLocal
from app.models.medication_schedule import MedicationSchedule
from app.models.call_log import CallLog
from app.services.voice_service import VoiceService
from app.models.patient import Patient

logger = logging.getLogger(__name__)

executors = {
    'default': ThreadPoolExecutor(10)
}
scheduler = AsyncIOScheduler(executors=executors)

def queue_daily_calls():
    now = datetime.now()
    current_time_str = now.strftime("%H:%M")
    
    db = SessionLocal()
    try:
        # Find active schedules triggering right at this precise minute
        schedules = db.query(MedicationSchedule).filter(
            MedicationSchedule.active == True,
            MedicationSchedule.time_to_call == current_time_str
        ).all()
        
        voice_service = VoiceService()
        
        for schedule in schedules:
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Check if a call was previously queued/attempted today for this specific patient
            existing_call = db.query(CallLog).filter(
                CallLog.patient_id == schedule.patient_id,
                CallLog.timestamp >= today_start
            ).first()
            
            if not existing_call:
                logger.info(f"Triggering outbound IVR adherence call for Patient {schedule.patient_id}")
                patient = db.query(Patient).filter(Patient.id == schedule.patient_id).first()
                if patient:
                    voice_service.initiate_call(patient.phone_number)
    except Exception as e:
        logger.error(f"Error in queue_daily_calls: {e}")
    finally:
        db.close()

def retry_failed_calls():
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    db = SessionLocal()
    try:
        failed_statuses = ["Failed", "Rejected", "NoAnswer", "Busy"]
        failed_calls = db.query(CallLog).filter(
            CallLog.timestamp >= today_start,
            CallLog.call_status.in_(failed_statuses)
        ).all()
        
        voice_service = VoiceService()
        patients_to_retry = set([c.patient_id for c in failed_calls])
        
        for patient_id in patients_to_retry:
            total_attempts = db.query(CallLog).filter(
                CallLog.patient_id == patient_id,
                CallLog.timestamp >= today_start
            ).count()
            
            # Skip if they succeeded eventually
            any_success = db.query(CallLog).filter(
                CallLog.patient_id == patient_id,
                CallLog.timestamp >= today_start,
                CallLog.call_status == "Completed"
            ).first()
            
            if not any_success and total_attempts < 3:
                logger.info(f"Retrying call to Patient {patient_id} (Attempt {total_attempts + 1})")
                patient = db.query(Patient).filter(Patient.id == patient_id).first()
                if patient:
                    voice_service.initiate_call(patient.phone_number)
    except Exception as e:
        logger.error(f"Error in retry_failed_calls: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler.add_job(queue_daily_calls, 'cron', minute='*')
    scheduler.add_job(retry_failed_calls, 'cron', minute='*/15')
    scheduler.start()
    logger.info("APScheduler background tasks dispatched.")

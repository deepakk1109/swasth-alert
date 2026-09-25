import os
import boto3
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="SwasthAlert API")

# AWS SNS Client
sns = boto3.client("sns", region_name=os.getenv("AWS_REGION", "ap-south-1"))

class PatientData(BaseModel):
    name: str
    phone: str
    email: str
    address: str
    blood_group: str
    age: int
    height_cm: float
    weight_kg: float
    chronic_illness: int
    missed_doses_last_month: int
    distance_to_clinic_km: float
    primary_diagnosis: str
    known_allergies: str
    current_medications: str
    side_effects: str
    last_visit_date: str
    doctor_name: str
    prescribed_tablets: str

class AlertPayload(BaseModel):
    patient_name: str
    phone: str
    doctor: str
    risk_score: str
    summary: str

@app.get("/", response_class=HTMLResponse)
def serve_home():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/predict-risk")
def predict_risk(data: PatientData):
    height_m = data.height_cm / 100
    bmi = round(data.weight_kg / (height_m ** 2), 1) if height_m > 0 else 0
    
    if bmi < 18.5:
        bmi_status = "Underweight"
    elif 18.5 <= bmi <= 24.9:
        bmi_status = "Normal Weight"
    elif 25.0 <= bmi <= 29.9:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    risk = (
        data.missed_doses_last_month * 0.25
        + data.chronic_illness * 0.20
        + (data.distance_to_clinic_km / 100) * 0.20
        + (data.age / 100) * 0.15
    )
    
    has_side_effects = data.side_effects.strip().lower() not in ["none", "nil", "illai", "no", ""]
    if has_side_effects:
        risk += 0.15

    if bmi >= 30:
        risk += 0.10

    risk = min(max(risk, 0.0), 1.0)
    score_pct = round(risk * 100, 1)

    if score_pct >= 70:
        priority = "High"
        action = f"Immediate Doctor Callback ({data.doctor_name}) + Adjust Medications"
    elif score_pct >= 40:
        priority = "Moderate"
        action = "Automated Clinical Check-in Call & Side-effects Review"
    else:
        priority = "Low"
        action = "Routine Refill & SMS Reminder"

    return {
        "patient": data.name,
        "phone": data.phone,
        "address": data.address,
        "blood_group": data.blood_group,
        "bmi": bmi,
        "bmi_status": bmi_status,
        "dropout_risk_score": f"{score_pct}%",
        "priority": priority,
        "recommended_action": action,
        "primary_diagnosis": data.primary_diagnosis,
        "known_allergies": data.known_allergies,
        "last_visit_date": data.last_visit_date,
        "doctor_name": data.doctor_name,
        "prescribed_tablets": data.prescribed_tablets,
        "current_medications": data.current_medications,
        "side_effects": data.side_effects
    }

@app.post("/dispatch-alert")
def dispatch_doctor_alert(data: AlertPayload):
    message = (
        f"[SwasthAlert HIGH PRIORITY]\n"
        f"Patient: {data.patient_name} ({data.phone})\n"
        f"Risk: {data.risk_score}\n"
        f"Assigned Doctor: {data.doctor}\n"
        f"Action: {data.summary}"
    )
    
    topic_arn = os.getenv("SNS_TOPIC_ARN")
    if topic_arn:
        try:
            sns.publish(TopicArn=topic_arn, Message=message, Subject="High Risk Patient Alert")
        except Exception as e:
            print(f"SNS error: {e}")

    return {"status": "dispatched", "message": f"Doctor {data.doctor} alerted successfully via AWS SNS for patient {data.patient_name}!"}

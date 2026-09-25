# SwasthAlert: AI-Powered Clinical Triage & UHID System

SwasthAlert is a decentralized, cross-hospital patient risk triage and continuous care platform designed to eliminate chronic treatment dropouts and medication non-adherence.

## 🚀 Live Deployment
- **Live URL:** http://65.1.95.222:8080
- **Cloud Infrastructure:** AWS EC2, AWS ECR, Docker, FastAPI

## 🏥 Problem Statement
Small healthcare centers and rural clinics suffer from high treatment dropout rates due to lack of follow-up visibility and fragmented patient records across hospitals.

## 💡 Core Architecture & Features
1. **Centralized UHID System:** Instant retrieval of cross-hospital records and multi-year consultation history using Universal Health IDs.
2. **AI Dropout Risk Scoring Engine:** Evaluates chronic condition severity, missed doses, and proximity to calculate clinical risk.
3. **Automated Emergency Dispatch:** GPS-ranked triage linking patients to nearby specialty centers and duty doctors.

## 🛠️ Tech Stack
- **Backend:** FastAPI, Python, Pydantic
- **Containerization:** Docker
- **Cloud & Orchestration:** AWS ECR, AWS EC2 (ap-south-1)
- **AI/Automation Partner:** Claude Code for automated container configuration and deployment pipelines.

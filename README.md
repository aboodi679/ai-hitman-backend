# AI Hitman — Cloud Backend

Cloud backend for **AI Hitman: Cloud Integrated Open World Sandbox Game**, a Final Year Project featuring zombie NPCs controlled by a hybrid FSM + Reinforcement Learning AI system.

This repository contains the AWS cloud infrastructure, REST API, and live stats dashboard. The Unity game client is maintained separately by my project partner.

🔗 **Live Dashboard:** http://hitman-npc-data.s3-website-us-east-1.amazonaws.com
🔗 **Live API:** https://4kbub5enwb.execute-api.us-east-1.amazonaws.com/production/ping

---

## What This Repo Does

- Provides a Flask REST API with 5 endpoints, deployed serverlessly on AWS Lambda
- Stores player game session statistics in AWS DynamoDB
- Hosts the trained Reinforcement Learning model in AWS S3, served to Unity at runtime
- Hosts a live public website showing real-time player stats
- Provisions all AWS infrastructure using Terraform (Infrastructure as Code)

---

## AI Design Note

The zombie NPCs in the game use a hybrid AI approach:
- **Finite State Machine (FSM)** controls all behavioral logic — Idle, Patrol, Chase, Attack, and Death
- **Reinforcement Learning**, trained with Unity ML-Agents, controls **only** zombie movement direction and speed

This backend stores which AI type (`FSM` or `RL`) was active during each recorded session.

---

## Repository Structure

```
ai-hitman-backend/
├── app.py                  # Flask API — 5 endpoints
├── requirements.txt         # Python dependencies
├── main.tf                  # Terraform: S3 + DynamoDB resources
├── variables.tf              # Terraform configuration variables
├── outputs.tf                 # Terraform output values
├── zappa_settings.json         # Zappa deployment configuration
├── index.html                   # Live stats dashboard website
└── README.md
```

---

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.8 |
| API Framework | Flask 3.0.3 |
| AWS SDK | boto3 |
| Deployment | Zappa (serverless) |
| Infrastructure | Terraform (HCL) |
| Compute | AWS Lambda |
| Routing | AWS API Gateway |
| Database | AWS DynamoDB |
| Storage | AWS S3 |

---

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/ping` | Health check — verifies the API is live |
| POST | `/save-session` | Saves player session stats (kills, weapon, health, time, AI type) |
| GET | `/get-stats` | Returns all sessions for the live dashboard |
| GET | `/get-model-url` | Returns a presigned S3 URL for the Unity client to download the RL model |
| POST | `/upload-model` | Uploads a newly trained RL model to S3 |

---

## Setup & Deployment

```bash
# Clone and enter the project
git clone https://github.com/YourUsername/ai-hitman-backend.git
cd ai-hitman-backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Fill in AWS credentials
# Create a .env file with:
# AWS_ACCESS_KEY_ID=...
# AWS_SECRET_ACCESS_KEY=...
# AWS_DEFAULT_REGION=us-east-1

# Provision AWS infrastructure
terraform init
terraform apply

# Deploy the API
zappa deploy production         # first-time deploy
zappa update production         # subsequent updates

# Update the live website after editing index.html
aws s3 cp index.html s3://hitman-npc-data/index.html --content-type "text/html"
```

---

## Team

| Member | Role |
|---|---|
| **Muhammad Abdullah** | Cloud & Backend Engineer (this repository) |
| **Hassan Saleh Hayat** | Game Developer & AI Engineer (Unity client) |

**Supervisor:** Mam Sana Fatima
**University:** University of Lahore, Sargodha Campus | BSSE | Session 2022–2026

---

## License

Developed as a Final Year Project for academic purposes.

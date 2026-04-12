# IVR Medication Adherence System

MVP for automated outward calls and DTMF adherence tracking leveraging Africa's Talking API.

## Requirements
- Python 3.11+
- PostgreSQL
- Africa's Talking Sandbox Account

## Setup Instructions
1. Clone the repository and navigate into it.
2. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in DB and Africa's Talking details.
   ```bash
   cp .env.example .env
   ```
5. Apply database migrations:
   ```bash
   alembic upgrade head
   ```
6. Start the FastAPI server locally:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Development & Testing with Ngrok
To receive Africa's Talking Voice webhooks locally, expose port 8000 using Ngrok:
```bash
ngrok http 8000
```
Copy your forwarding URL (e.g., `https://abcdef.ngrok.io`) and update `BASE_URL` in `.env`.
Go to Africa's Talking Sandbox dashboard:
1. Voice -> Phone Numbers -> Webhooks.
2. Set the *Callback URL* to `https://abcdef.ngrok.io/voice/instruct`.
3. Set the *Events Callback URL* to `https://abcdef.ngrok.io/voice/events`.

## Sandbox Testing Steps
1. Launch ngrok and start the server.
2. Ensure you have seeded patients via `python scripts/seed_data.py`.
3. Go to the AT Sandbox simulator tool.
4. If you fire an outbound call matching a patient's schedule time, the AT API will hit your Ngrok URL.

## Thesis Objectives Fulfilled
This MVP covers automated patient syncing, CRON-based scheduling, resilient queue handling, and pure DTMF IVR interactions across multiple local dialects to ensure maximal systemic adherence captures without relying on app presence.

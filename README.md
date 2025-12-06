# SainathAI Pinterest Engine - Fixed Repo

This repo contains a minimal Pinterest Engine prepared for Hugging Face Spaces (Docker mode).
Files added by the audit:
- Dockerfile
- requirements.txt
- app.py
- engine.py
- .github/workflows/ci.yml

Usage:
- Set HF_TOKEN as an environment variable in Hugging Face Space (if using HF APIs).
- Build with Docker or deploy to HF Space (Docker mode).
- Run locally: `uvicorn app:app --host 0.0.0.0 --port 7860`
